from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.services.resume_parser import ResumeParser

router = APIRouter()

# 初始化 ResumeSDK 解析器
parser = ResumeParser()


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    """
    上传并解析简历文件

    使用 ResumeSDK API 解析简历，提取所有字段信息。
    支持 PDF、Word 等多种格式。
    """
    # 保存上传的文件到临时目录
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_path = tmp_file.name

    try:
        # 使用 ResumeSDK 解析简历
        parsed_data = await parser.parse(tmp_path, file_name=file.filename)

        # 构建完整的响应数据
        response = {
            "success": True,
            "filename": file.filename,
            "file_size": len(content),
            "parsed_data": parsed_data,
            # 提取关键字段便于前端展示
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
            # 字段验证状态
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

        return response

    except Exception as e:
        return {
            "success": False,
            "filename": file.filename,
            "error": str(e),
            "error_type": type(e).__name__,
        }
    finally:
        # 清理临时文件
        try:
            Path(tmp_path).unlink(missing_ok=True)
        except:
            pass


@router.get("/{resume_id}")
async def get_resume(resume_id: str) -> dict:
    """Get parsed resume by ID."""
    # TODO: Implement resume retrieval
    return {"resume_id": resume_id}


@router.get("/{resume_id}/gaps")
async def analyze_resume_gaps(resume_id: str) -> dict:
    """Analyze resume for gaps and issues."""
    # TODO: Implement gap analysis
    return {"resume_id": resume_id, "gaps": []}
