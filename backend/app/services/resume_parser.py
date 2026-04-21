"""
ResumeSDK 简历解析服务

使用 ResumeSDK API 进行简历解析，支持 PDF、Word 等多种格式。
文档: https://www.resumesdk.com/docs/rs-parser.html

创建时间: 2026-04-21
"""

from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

import httpx
from app.config import settings


class ResumeParser:
    """
    ResumeSDK 简历解析器

    使用 ResumeSDK API 解析简历，支持 40+ 种格式，180+ 字段识别。

    Attributes:
        api_url: ResumeSDK API 地址
        uid: 用户ID
        pwd: 密码

    Example:
        >>> parser = ResumeParser()
        >>> result = parser.parse("/path/to/resume.pdf")
        >>> print(f"姓名: {result['name']}")
    """

    # ResumeSDK SaaS API 地址
    DEFAULT_API_URL = "http://www.resumesdk.com/api/parse"

    def __init__(self, api_url: str | None = None, uid: str | None = None, pwd: str | None = None) -> None:
        """
        初始化 ResumeSDK 解析器

        Args:
            api_url: API 地址，默认使用 SaaS 地址
            uid: ResumeSDK 用户ID，默认从配置读取
            pwd: ResumeSDK 密码，默认从配置读取
        """
        self.api_url = api_url or getattr(settings, 'RESUMESDK_API_URL', self.DEFAULT_API_URL)
        self.uid = uid or getattr(settings, 'RESUMESDK_UID', '')
        self.pwd = pwd or getattr(settings, 'RESUMESDK_PWD', '')

    def _read_file(self, file_path: str) -> bytes:
        """
        读取文件内容

        Args:
            file_path: 文件路径

        Returns:
            bytes: 文件二进制内容
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        return path.read_bytes()

    def _build_request(self, file_path: str, file_name: str | None = None) -> dict[str, Any]:
        """
        构建 API 请求数据

        Args:
            file_path: 文件路径
            file_name: 文件名（可选）

        Returns:
            dict: 请求数据
        """
        file_content = self._read_file(file_path)
        file_cont_base64 = base64.b64encode(file_content).decode('utf-8')

        return {
            "file_name": file_name or Path(file_path).name,
            "file_cont": file_cont_base64,
        }

    def _transform_result(self, sdk_result: dict[str, Any]) -> dict[str, Any]:
        """
        将 ResumeSDK 结果转换为系统标准格式

        Args:
            sdk_result: ResumeSDK 返回的原始结果

        Returns:
            dict: 转换后的标准格式
        """
        result = sdk_result.get("result", {})

        # 提取教育背景
        education = []
        for edu in result.get("education_objs", []):
            education.append({
                "school": edu.get("school", ""),
                "degree": edu.get("degree", ""),
                "major": edu.get("major", ""),
                "start_date": edu.get("start_date", ""),
                "end_date": edu.get("end_date", ""),
            })

        # 提取工作经历
        experiences = []
        for exp in result.get("job_exp_objs", []):
            experiences.append({
                "company": exp.get("company", ""),
                "title": exp.get("title", ""),
                "start_date": exp.get("start_date", ""),
                "end_date": exp.get("end_date", ""),
                "description": exp.get("description", ""),
            })

        # 提取技能
        skills = result.get("skills", "").split(",") if result.get("skills") else []
        skills = [s.strip() for s in skills if s.strip()]

        # 合并个人总结和个人简介
        # ResumeSDK 可能使用不同字段返回个人总结：self_evaluation 或 cont_my_desc
        summary = result.get("self_evaluation", "")
        if not summary:
            # 尝试从 cont_my_desc 获取（ResumeSDK 对个人总结的另一种返回方式）
            summary = result.get("cont_my_desc", "")
        if not summary:
            # 尝试从 personal_summary 获取
            summary = result.get("personal_summary", "")

        # 提取技能对象（用于标签云）
        skills_objs = result.get("skills_objs", [])

        # 提取评估数据
        eval_data = sdk_result.get("eval", {})

        # 提取标签数据
        tags_data = sdk_result.get("tags", {})

        return {
            "name": result.get("name", ""),
            "email": result.get("email", ""),
            "phone": result.get("phone", ""),
            "gender": result.get("gender", ""),
            "age": result.get("age", 0),
            "location": result.get("location", ""),
            "summary": summary,
            "skills": skills,
            "skills_objs": skills_objs,
            "education": education,
            "experiences": experiences,
            "eval": eval_data,
            "tags": tags_data,
            "resume_integrity": result.get("resume_integrity", 0),
            "raw_result": sdk_result,  # 保留原始结果
        }

    async def parse(self, file_path: str, file_name: str | None = None) -> dict[str, Any]:
        """
        解析简历文件

        Args:
            file_path: 简历文件路径
            file_name: 文件名（可选）

        Returns:
            dict: 解析结果

        Raises:
            RuntimeError: API 调用失败
            FileNotFoundError: 文件不存在
        """
        # 构建请求
        request_data = self._build_request(file_path, file_name)

        # 设置请求头
        headers = {
            "Content-Type": "application/json",
            "uid": self.uid,
            "pwd": self.pwd,
        }

        # 调用 API
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=request_data,
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as e:
                raise RuntimeError(f"ResumeSDK API 错误: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                raise RuntimeError(f"请求 ResumeSDK API 失败: {e}")

        # 解析响应
        result = response.json()

        # 检查状态码
        status = result.get("status", {})
        if status.get("code") != 200:
            raise RuntimeError(f"ResumeSDK 解析失败: {status.get('message', '未知错误')}")

        # 转换结果
        parsed_data = self._transform_result(result)

        # 添加元数据
        parsed_data["_meta"] = {
            "file_path": file_path,
            "parser": "resumesdk",
            "api_url": self.api_url,
            "account": result.get("account", {}),
        }

        return parsed_data

    def parse_sync(self, file_path: str, file_name: str | None = None) -> dict[str, Any]:
        """
        同步解析简历文件（用于非异步环境）

        Args:
            file_path: 简历文件路径
            file_name: 文件名（可选）

        Returns:
            dict: 解析结果
        """
        import asyncio
        return asyncio.run(self.parse(file_path, file_name))

    async def parse_batch(self, file_paths: list[str]) -> list[dict[str, Any]]:
        """
        批量解析简历

        Args:
            file_paths: 简历文件路径列表

        Returns:
            list: 解析结果列表
        """
        results = []
        for file_path in file_paths:
            try:
                result = await self.parse(file_path)
                results.append({"success": True, "data": result})
            except Exception as e:
                results.append({"success": False, "error": str(e), "file_path": file_path})
        return results

    def get_account_info(self) -> dict[str, Any]:
        """
        获取账户信息

        Returns:
            dict: 账户信息
        """
        return {
            "uid": self.uid,
            "api_url": self.api_url,
            "configured": bool(self.uid and self.pwd),
        }
