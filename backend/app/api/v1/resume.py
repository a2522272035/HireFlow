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
        # 调试：打印解析器配置
        print(f"[DEBUG] Parser config: api_url={parser.api_url}, uid={parser.uid}, need_avatar will be sent")
        
        # 使用 ResumeSDK 解析简历
        parsed_data = await parser.parse(tmp_path, file_name=file.filename)
        
        # 调试：打印原始响应中的头像字段
        raw_result = parsed_data.get("raw_result", {})
        result_data = raw_result.get("result", {})
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
        response = {
            "success": True,
            "filename": file.filename,
            "file_size": len(content),
            "parsed_data": parsed_data,
            # 添加原始 ResumeSDK 响应供调试
            "raw_resumesdk_response": parsed_data.get("raw_result", {}),
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
        # 确保错误消息不包含非ASCII字符，避免GBK编码问题
        error_msg = str(e).encode('ascii', 'replace').decode('ascii')
        return {
            "success": False,
            "filename": file.filename,
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
async def get_resume(resume_id: str) -> dict:
    """Get parsed resume by ID."""
    # TODO: Implement resume retrieval
    return {"resume_id": resume_id}


@router.get("/{resume_id}/gaps")
async def analyze_resume_gaps(resume_id: str) -> dict:
    """Analyze resume for gaps and issues."""
    # TODO: Implement gap analysis
    return {"resume_id": resume_id, "gaps": []}
