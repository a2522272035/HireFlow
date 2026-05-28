from __future__ import annotations

import hashlib
import json
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.core.database import get_db
from app.models.resume import Resume, ResumeExperience, ResumeSkill
from app.services.resume_parser import ResumeParser

router = APIRouter()

# 初始化 ResumeSDK 解析器
parser = ResumeParser()


def _safe_file_name(filename: str | None) -> str:
    name = Path(filename or "resume").name.strip()
    return name or "resume"


def _candidate_name(parsed_data: dict) -> str:
    return str(parsed_data.get("name") or parsed_data.get("candidate_name") or "未知候选人").strip()


def _candidate_target_position(parsed_data: dict) -> str:
    return str(
        parsed_data.get("expect_job")
        or parsed_data.get("expected_job")
        or parsed_data.get("work_position")
        or parsed_data.get("current_position")
        or parsed_data.get("position")
        or ""
    ).strip()


def _candidate_identity(parsed_data: dict) -> tuple[str, str, str, str, str, str, str | None]:
    name = _candidate_name(parsed_data)
    phone = str(parsed_data.get("phone") or parsed_data.get("mobile") or "").strip()
    email = str(parsed_data.get("email") or parsed_data.get("e_mail") or "").strip()
    target_position = _candidate_target_position(parsed_data)
    identity_key = "|".join(part for part in (name, phone, email, target_position) if part)
    if identity_key:
        candidate_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"hireflow-candidate:{identity_key}"))
    else:
        candidate_id = str(uuid.uuid4())
    candidate_fingerprint = hashlib.sha256(identity_key.encode("utf-8")).hexdigest() if identity_key else None
    return candidate_id, name, phone, email, target_position, identity_key, candidate_fingerprint


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _sha256_text(content: str) -> str | None:
    normalized = " ".join((content or "").split())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest() if normalized else None


def _str_or_none(value: object) -> str | None:
    text_value = str(value).strip() if value is not None else ""
    return text_value or None


def _int_or_none(value: object) -> int | None:
    try:
        return int(value) if value not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _resume_raw_content(parsed_data: dict) -> str:
    return str(
        parsed_data.get("raw_text")
        or parsed_data.get("summary")
        or parsed_data.get("self_evaluation")
        or ""
    )


async def _ensure_live_resume_columns(db: AsyncSession) -> None:
    for statement in (
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS name varchar(100)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS original_filename varchar(500)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_type varchar(50)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_name varchar(100)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_email varchar(255)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_phone varchar(50)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_path text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS raw_content text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parsed_data jsonb DEFAULT '{}'::jsonb",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS status varchar(50) DEFAULT 'pending'",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS created_at timestamp with time zone DEFAULT now()",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS updated_at timestamp with time zone DEFAULT now()",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_id text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_fingerprint text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_gender varchar(20)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_age integer",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS candidate_location varchar(100)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS school varchar(200)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS degree varchar(100)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS major varchar(200)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS work_year varchar(50)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS current_position varchar(200)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS current_company varchar(200)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS expect_job varchar(200)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS expect_salary varchar(100)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS resume_integrity varchar(50)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_name text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_size integer",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS file_sha256 varchar(64)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS content_sha256 varchar(64)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parsed_json jsonb DEFAULT '{}'::jsonb",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS raw_sdk_response jsonb DEFAULT '{}'::jsonb",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parsed_text text",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parser_name varchar(50) DEFAULT 'resumesdk'",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parser_version varchar(50)",
        "ALTER TABLE resumes ADD COLUMN IF NOT EXISTS parsed_at timestamp with time zone",
        "ALTER TABLE resume_skills ADD COLUMN IF NOT EXISTS skill varchar(100)",
        "ALTER TABLE resume_skills ADD COLUMN IF NOT EXISTS skill_name varchar(100)",
        "ALTER TABLE resume_skills ADD COLUMN IF NOT EXISTS years_of_experience integer",
        "ALTER TABLE resume_skills ADD COLUMN IF NOT EXISTS years_experience integer",
        "ALTER TABLE resume_experiences ADD COLUMN IF NOT EXISTS position varchar(200)",
        "ALTER TABLE resume_experiences ADD COLUMN IF NOT EXISTS title varchar(200)",
        "ALTER TABLE resume_experiences ADD COLUMN IF NOT EXISTS is_current varchar(10) DEFAULT 'false'",
        "CREATE INDEX IF NOT EXISTS ix_resumes_file_sha256 ON resumes(file_sha256)",
        "CREATE INDEX IF NOT EXISTS ix_resumes_content_sha256 ON resumes(content_sha256)",
        "CREATE INDEX IF NOT EXISTS ix_resumes_candidate_fingerprint ON resumes(candidate_fingerprint)",
    ):
        await db.execute(text(statement))


async def _upsert_live_candidate_if_available(
    db: AsyncSession,
    candidate_id: str,
    name: str,
    phone: str,
    email: str,
    target_position: str,
    identity_key: str,
) -> None:
    result = await db.execute(text("SELECT to_regclass('public.candidates')"))
    if result.scalar_one_or_none() is None:
        return
    await db.execute(
        text(
            """
            INSERT INTO candidates (id, name, phone, email, target_position, identity_key)
            VALUES (:id, :name, :phone, :email, :target_position, :identity_key)
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                email = EXCLUDED.email,
                target_position = EXCLUDED.target_position,
                identity_key = EXCLUDED.identity_key,
                updated_at = now()
            """
        ),
        {
            "id": candidate_id,
            "name": name,
            "phone": phone,
            "email": email,
            "target_position": target_position,
            "identity_key": identity_key,
        },
    )


async def _find_cached_resume(db: AsyncSession, file_sha256: str) -> Resume | None:
    result = await db.execute(
        select(Resume)
        .where(Resume.file_sha256 == file_sha256, Resume.status == "parsed")
        .order_by(Resume.updated_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


def _skill_name(skill: object) -> str:
    if isinstance(skill, str):
        return skill.strip()
    if isinstance(skill, dict):
        return str(skill.get("skills_name") or skill.get("skill_name") or skill.get("name") or "").strip()
    return ""


def _experience_value(job: dict, *keys: str) -> str:
    for key in keys:
        value = job.get(key)
        if value:
            return str(value).strip()
    return ""


def _save_resume_sections(resume_record: Resume, parsed_data: dict) -> None:
    raw_skills = parsed_data.get("skills_objs") or parsed_data.get("skills") or []
    if isinstance(raw_skills, list):
        for skill in raw_skills:
            skill_name = _skill_name(skill)
            if skill_name:
                skill_value = skill_name[:100]
                resume_record.skills.append(ResumeSkill(skill=skill_value, skill_name=skill_value))

    raw_experiences = parsed_data.get("job_exp_objs") or parsed_data.get("experiences") or []
    if isinstance(raw_experiences, list):
        for job in raw_experiences:
            if not isinstance(job, dict):
                continue
            company = _experience_value(job, "job_cpy", "job_company", "company") or "未提供"
            title = _experience_value(job, "job_position", "job_pos_name", "position", "title") or "未提供"
            title_value = title[:200]
            description = _experience_value(job, "job_content", "job_desc", "description")
            resume_record.experiences.append(
                ResumeExperience(
                    company=company[:200],
                    position=title_value,
                    title=title_value,
                    is_current="true" if _experience_value(job, "end_date") in {"至今", "now", "present"} else "false",
                    description=description,
                )
            )


def _build_upload_response(
    *,
    resume_record: Resume,
    parsed_data: dict,
    filename: str,
    file_size: int,
    cache_hit: bool,
    database_status: str | None = None,
    database_warning: str | None = None,
) -> dict:
    raw_sdk_response = resume_record.raw_sdk_response or parsed_data.get("raw_result", {})
    return {
        "success": True,
        "cache_hit": cache_hit,
        "resume_id": str(resume_record.id),
        "candidate_id": resume_record.candidate_id,
        "candidate_fingerprint": resume_record.candidate_fingerprint,
        "filename": filename,
        "file_size": file_size,
        "file_path": resume_record.file_path,
        "file_sha256": resume_record.file_sha256,
        "content_sha256": resume_record.content_sha256,
        "database": {
            "status": database_status or ("cache_hit" if cache_hit else "saved"),
            "table": "resumes",
            "json_fields": ["parsed_data", "parsed_json", "raw_sdk_response"],
            "indexed_fields": ["file_sha256", "content_sha256", "candidate_fingerprint"],
            "warning": database_warning,
        },
        "parsed_data": parsed_data,
        "raw_resumesdk_response": raw_sdk_response,
        "extracted_fields": {
            "name": parsed_data.get("name"),
            "email": parsed_data.get("email"),
            "phone": parsed_data.get("phone"),
            "gender": parsed_data.get("gender"),
            "age": parsed_data.get("age"),
            "location": parsed_data.get("location"),
            "summary": parsed_data.get("summary"),
            "skills": parsed_data.get("skills", []),
            "education": parsed_data.get("education", []),
            "experiences": parsed_data.get("experiences", []),
        },
        "indexed_profile": {
            "gender": resume_record.candidate_gender,
            "age": resume_record.candidate_age,
            "location": resume_record.candidate_location,
            "school": resume_record.school,
            "degree": resume_record.degree,
            "major": resume_record.major,
            "work_year": resume_record.work_year,
            "current_position": resume_record.current_position,
            "current_company": resume_record.current_company,
            "expect_job": resume_record.expect_job,
            "expect_salary": resume_record.expect_salary,
            "resume_integrity": resume_record.resume_integrity,
        },
        "field_status": {
            "name": "ok" if parsed_data.get("name") else "missing",
            "email": "ok" if parsed_data.get("email") else "missing",
            "phone": "ok" if parsed_data.get("phone") else "missing",
            "gender": "ok" if parsed_data.get("gender") else "missing",
            "age": "ok" if parsed_data.get("age") else "missing",
            "location": "ok" if parsed_data.get("location") else "missing",
            "summary": "ok" if parsed_data.get("summary") else "missing",
            "skills": "ok" if parsed_data.get("skills") else "missing",
            "education": "ok" if parsed_data.get("education") else "missing",
            "experiences": "ok" if parsed_data.get("experiences") else "missing",
        },
        "meta": parsed_data.get("_meta", {}),
    }


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)) -> dict:
    """
    上传并解析简历文件

    使用 ResumeSDK API 解析简历，提取所有字段信息。
    支持 PDF、Word 等多种格式。
    """
    # 保存上传的文件到临时目录
    original_name = _safe_file_name(file.filename)
    suffix = Path(original_name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        file_sha256 = _sha256_bytes(content)
        db_available = True
        database_warning = None

        try:
            await _ensure_live_resume_columns(db)
            cached_resume = await _find_cached_resume(db, file_sha256)
            if cached_resume:
                parsed_data = cached_resume.parsed_data or cached_resume.parsed_json or {}
                return _build_upload_response(
                    resume_record=cached_resume,
                    parsed_data=parsed_data,
                    filename=cached_resume.file_name or original_name,
                    file_size=cached_resume.file_size or len(content),
                    cache_hit=True,
                )
        except SQLAlchemyError as db_error:
            await db.rollback()
            db_available = False
            database_warning = f"database cache unavailable: {db_error.__class__.__name__}"

        # 调试：打印解析器配置
        print(f"[DEBUG] Parser config: api_url={parser.api_url}, uid={parser.uid}, need_avatar will be sent")
        
        # 使用 ResumeSDK 解析简历
        parsed_data = await parser.parse(tmp_path, file_name=original_name)
        candidate_id, name, phone, email, target_position, identity_key, candidate_fingerprint = _candidate_identity(parsed_data)
        resume_id = uuid.uuid4()
        upload_dir = Path(settings.UPLOAD_DIR) / "resumes"
        upload_dir.mkdir(parents=True, exist_ok=True)
        stored_filename = f"{resume_id}{suffix or '.resume'}"
        stored_path = upload_dir / stored_filename
        stored_path.write_bytes(content)
        raw_content = _resume_raw_content(parsed_data)
        parsed_text = json.dumps(parsed_data, ensure_ascii=False)[:12000]

        resume_record = Resume(
            id=resume_id,
            name=name,
            original_filename=original_name,
            file_type=suffix.lstrip(".") or None,
            candidate_name=name,
            candidate_email=email or None,
            candidate_phone=phone or None,
            candidate_gender=_str_or_none(parsed_data.get("gender")),
            candidate_age=_int_or_none(parsed_data.get("age")),
            candidate_location=_str_or_none(parsed_data.get("location") or parsed_data.get("expect_jlocation_norm")),
            candidate_id=candidate_id,
            candidate_fingerprint=candidate_fingerprint,
            school=_str_or_none(parsed_data.get("college")),
            degree=_str_or_none(parsed_data.get("degree")),
            major=_str_or_none(parsed_data.get("major")),
            work_year=_str_or_none(parsed_data.get("work_year_norm") or parsed_data.get("work_year")),
            current_position=_str_or_none(parsed_data.get("work_position") or parsed_data.get("current_job_title")),
            current_company=_str_or_none(parsed_data.get("work_company") or parsed_data.get("current_company")),
            expect_job=_str_or_none(parsed_data.get("expect_job")),
            expect_salary=_str_or_none(parsed_data.get("expect_salary")),
            resume_integrity=_str_or_none(parsed_data.get("resume_integrity")),
            file_name=original_name,
            file_size=len(content),
            file_sha256=file_sha256,
            content_sha256=_sha256_text(raw_content),
            file_path=str(stored_path),
            raw_content=raw_content,
            parsed_data=parsed_data,
            parsed_json=parsed_data,
            raw_sdk_response=parsed_data.get("raw_result", {}),
            parsed_text=parsed_text,
            parser_name="resumesdk",
            parsed_at=datetime.now(timezone.utc),
            status="parsed",
        )
        _save_resume_sections(resume_record, parsed_data)

        database_status = "saved"
        if db_available:
            try:
                await _upsert_live_candidate_if_available(
                    db,
                    candidate_id=candidate_id,
                    name=name,
                    phone=phone,
                    email=email,
                    target_position=target_position,
                    identity_key=identity_key,
                )
                db.add(resume_record)
                await db.flush()
                await db.commit()
            except SQLAlchemyError as db_error:
                await db.rollback()
                database_status = "save_failed"
                database_warning = f"database save failed: {db_error.__class__.__name__}"
        else:
            database_status = "unavailable"
        
        # 调试：打印原始响应中的头像字段
        raw_result = parsed_data.get("raw_result", {})
        result_data = raw_result.get("result", {}) if isinstance(raw_result, dict) else {}
        if not isinstance(result_data, dict):
            result_data = {}
        print(f"[DEBUG] ResumeSDK response avatar_url: {result_data.get('avatar_url', 'None')}")
        print(f"[DEBUG] ResumeSDK response avatar_data: {'Present' if result_data.get('avatar_data') else 'None'}")
        
        # 调试：打印转换后的 parsed_data 中的头像字段
        print(f"[DEBUG] parsed_data.avatar_data (根级别): {'Present' if parsed_data.get('avatar_data') else 'None'}")
        if parsed_data.get('avatar_data'):
            print(f"[DEBUG] parsed_data.avatar_data length: {len(parsed_data['avatar_data'])}")
            # 安全打印预览，避免编码问题
            avatar_preview = parsed_data['avatar_data'][:50]
            try:
                print(f"[DEBUG] parsed_data.avatar_data preview: {avatar_preview}...")
            except UnicodeEncodeError:
                print(f"[DEBUG] parsed_data.avatar_data preview: [包含非ASCII字符，已跳过详细打印]")

        # 构建完整的响应数据
        return _build_upload_response(
            resume_record=resume_record,
            parsed_data=parsed_data,
            filename=original_name,
            file_size=len(content),
            cache_hit=False,
            database_status=database_status,
            database_warning=database_warning,
        )

    except Exception as e:
        await db.rollback()
        # 确保错误消息不包含非ASCII字符，避免GBK编码问题
        error_msg = str(e).encode('ascii', 'replace').decode('ascii')
        return {
            "success": False,
            "filename": original_name,
            "error": error_msg,
            "error_type": type(e).__name__,
        }
    finally:
        # 清理临时文件
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except:
            pass


@router.get("/{resume_id}")
async def get_resume(resume_id: str, db: AsyncSession = Depends(get_db)) -> dict:
    """Get parsed resume by ID."""
    await _ensure_live_resume_columns(db)
    try:
        resume_uuid = uuid.UUID(resume_id)
    except ValueError:
        return {"success": False, "error": "Invalid resume_id"}

    result = await db.execute(select(Resume).where(Resume.id == resume_uuid))
    resume_record = result.scalar_one_or_none()
    if not resume_record:
        return {"success": False, "error": "Resume not found", "resume_id": resume_id}

    parsed_data = resume_record.parsed_data or resume_record.parsed_json or {}
    return {
        "success": True,
        "resume_id": str(resume_record.id),
        "candidate_id": resume_record.candidate_id,
        "candidate_fingerprint": resume_record.candidate_fingerprint,
        "filename": resume_record.file_name,
        "file_path": resume_record.file_path,
        "file_sha256": resume_record.file_sha256,
        "content_sha256": resume_record.content_sha256,
        "status": resume_record.status,
        "parsed_at": resume_record.parsed_at.isoformat() if resume_record.parsed_at else None,
        "indexed_profile": {
            "gender": resume_record.candidate_gender,
            "age": resume_record.candidate_age,
            "location": resume_record.candidate_location,
            "school": resume_record.school,
            "degree": resume_record.degree,
            "major": resume_record.major,
            "work_year": resume_record.work_year,
            "current_position": resume_record.current_position,
            "current_company": resume_record.current_company,
            "expect_job": resume_record.expect_job,
            "expect_salary": resume_record.expect_salary,
            "resume_integrity": resume_record.resume_integrity,
        },
        "parsed_data": parsed_data,
        "raw_resumesdk_response": resume_record.raw_sdk_response or parsed_data.get("raw_result", {}),
    }


@router.get("/{resume_id}/gaps")
async def analyze_resume_gaps(resume_id: str) -> dict:
    """Analyze resume for gaps and issues."""
    # TODO: Implement gap analysis
    return {"resume_id": resume_id, "gaps": []}
