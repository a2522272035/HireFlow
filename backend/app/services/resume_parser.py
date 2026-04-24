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

    @staticmethod
    def _safe_str(s: Any) -> str:
        """
        将任意值转换为字符串，并确保可以安全编码为 GBK/UTF-8（替换非 ASCII 字符）
        
        Args:
            s: 任意值
            
        Returns:
            ASCII 安全的字符串
        """
        if not isinstance(s, str):
            s = str(s)
        # 替换非 ASCII 字符为 '?'
        return s.encode('ascii', 'replace').decode('ascii')

    @staticmethod
    def _map_college_type(college_type_code: str) -> str:
        """
        将学校类型代码映射为可读的文本
        
        Args:
            college_type_code: 学校类型代码
            
        Returns:
            学校类型文本
        """
        college_type_mapping = {
            "1": "普通本科",
            "2": "211高校",
            "3": "985高校",
            "4": "双一流高校",
            "5": "普通专科",
            "6": "职业教育",
            "7": "海外高校",
            "8": "其他"
        }
        return college_type_mapping.get(college_type_code, "未知")

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

    def _build_request(self, file_path: str, file_name: str | None = None) -> tuple[dict[str, Any], dict[str, str]]:
        """
        构建 API 请求数据

        Args:
            file_path: 文件路径
            file_name: 文件名（可选）

        Returns:
            tuple: (请求体数据, 请求头)
                   uid 和 pwd 需要放在 JSON body 中（ResumeSDK API 要求）
                   need_avatar 需要放在 JSON body 中
        """
        file_content = self._read_file(file_path)
        file_cont_base64 = base64.b64encode(file_content).decode('utf-8')

        # JSON body：包含文件内容和 need_avatar 参数，uid 和 pwd 按照 ResumeSDK 要求放在 body 中
        body_data = {
            "uid": self.uid,
            "pwd": self.pwd,
            "file_name": file_name or Path(file_path).name,
            "file_cont": file_cont_base64,
            "need_avatar": 1,  # 启用头像解析（关键参数！否则服务端不会返回头像数据）
        }

        # HTTP headers：完全模拟浏览器请求，确保头像解析正常
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Host": "www.resumesdk.com",
            "Origin": "http://www.resumesdk.com",
            "Referer": "http://www.resumesdk.com/",
        }

        return body_data, headers

    def _transform_result(self, sdk_result: dict[str, Any]) -> dict[str, Any]:
        """
        将 ResumeSDK 结果转换为系统标准格式

        Args:
            sdk_result: ResumeSDK 返回的原始结果

        Returns:
            dict: 转换后的标准格式
        """
        result = sdk_result.get("result", {})
        
        # 处理头像数据
        avatar_url = result.get("avatar_url", "")
        avatar_data_raw = result.get("avatar_data", "")
        avatar_data = avatar_data_raw
        if avatar_data_raw and not avatar_data_raw.startswith("data:image"):
            # 如果头像数据是纯 base64 字符串，添加 data URL 前缀
            avatar_data = f"data:image/jpeg;base64,{avatar_data_raw.strip()}"
        
        # 提取教育背景
        education = []
        for edu in result.get("education_objs", []):
            education.append({
                "school": edu.get("edu_college", ""),
                "degree": edu.get("edu_degree", ""),
                "major": edu.get("edu_major", ""),
                "start_date": edu.get("start_date", ""),
                "end_date": edu.get("end_date", ""),
            })

        # 提取工作经历
        experiences = []
        for exp in result.get("job_exp_objs", []):
            experiences.append({
                "company": exp.get("job_cpy", ""),
                "title": exp.get("job_position", ""),
                "start_date": exp.get("start_date", ""),
                "end_date": exp.get("end_date", ""),
                "description": exp.get("job_content", ""),
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

        # 提取毕业学校类型并映射
        college_type_code = result.get("college_type", "")
        college_type = self._map_college_type(college_type_code)
        
        # 提取毕业时间
        graduation_time = result.get("grad_time", "")
        
        # 提取参加工作时间
        work_start_time = result.get("work_start_time", "")
        work_start_time_inferred = result.get("work_start_time_inf", "")
        
        # 提取当前职能类型
        work_pos_type_p = result.get("work_pos_type_p", "")
        
        # 提取规范化工作年限
        work_year_norm = result.get("work_year_norm", "")
        
        return {
            # 基本信息
            "name": result.get("name", ""),
            "email": result.get("email", ""),
            "phone": result.get("phone", ""),
            "gender": result.get("gender", ""),
            "age": result.get("age", 0),
            "location": result.get("location", ""),
            "avatar_url": avatar_url,  # 头像URL
            "avatar_data": avatar_data,  # 头像Base64数据（已确保为完整 data URL）
            
            # 教育和职业信息
            "degree": result.get("degree", ""),
            "college": result.get("college", ""),
            "major": result.get("major", ""),
            "work_year": result.get("work_year", 0),
            "work_position": result.get("work_position", ""),
            "work_company": result.get("work_company", ""),
            
            # 新增字段（匹配简历解析.txt）
            "graduation_time": graduation_time,
            "college_type": college_type,
            "work_start_time": work_start_time,
            "work_start_time_inferred": work_start_time_inferred,
            "work_pos_type_p": work_pos_type_p,
            "work_year_norm": work_year_norm,
            
            # 期望工作
            "expect_salary": result.get("expect_salary", ""),
            "expect_job": result.get("expect_job", ""),
            "desired_location": result.get("desired_location", ""),
            "expect_salary_min": result.get("expect_salary_min", ""),
            "expect_salary_max": result.get("expect_salary_max", ""),
            "expect_jlocation": result.get("expect_jlocation", ""),
            "expect_jlocation_norm": result.get("expect_jlocation_norm", ""),
            
            # 其他字段
            "summary": summary,
            "skills": skills,
            "skills_objs": skills_objs,
            "education": education,
            "education_objs": result.get("education_objs", []),  # 保留原始教育经历对象数组
            "experiences": experiences,
            "job_exp_objs": result.get("job_exp_objs", []),  # 保留原始工作经历对象数组
            "eval": eval_data,
            "tags": tags_data,
            "resume_integrity": result.get("resume_integrity", 0),
            "lang": result.get("lang", "zh"),
            "current_job_title": result.get("current_job_title", ""),
            "current_company": result.get("current_company", ""),
            "desired_job_title": result.get("desired_job_title", ""),
            "desired_salary": result.get("desired_salary", ""),
            "self_evaluation": result.get("self_evaluation", ""),
            "cont_my_desc": result.get("cont_my_desc", ""),
            "personal_summary": result.get("personal_summary", ""),
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
        # 构建请求（返回 body 和 headers）
        request_data, headers = self._build_request(file_path, file_name)
        
        # 保存请求数据到文件用于调试
        import json as json_module
        debug_request = {k: v for k, v in request_data.items() if k != 'file_cont'}
        debug_request['file_cont_length'] = len(request_data.get('file_cont', ''))
        with open('debug_resumesdk_request.json', 'w', encoding='utf-8') as f:
            json_module.dump(debug_request, f, ensure_ascii=False, indent=2)
        
        # 调试：打印请求配置
        print(f"[DEBUG] Sending request to ResumeSDK API: {self.api_url}")
        print(f"[DEBUG] Request body keys: {list(request_data.keys())}")
        print(f"[DEBUG] need_avatar value: {request_data.get('need_avatar')}")
        print(f"[DEBUG] Headers uid: {headers.get('uid')}")
        print(f"[DEBUG] Debug request saved to debug_resumesdk_request.json")

        # 调用 API - uid/pwd 在 headers 中，need_avatar 在 JSON body 中
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=request_data,
                )
                response.raise_for_status()
                
                # 调试：打印响应状态和关键信息
                print(f"[DEBUG] ResumeSDK API Response Status: {response.status_code}")
                response_json = response.json()
                
                # 保存完整响应到文件用于调试
                with open('debug_resumesdk_response.json', 'w', encoding='utf-8') as f:
                    json_module.dump(response_json, f, ensure_ascii=False, indent=2)
                print(f"[DEBUG] Full response saved to debug_resumesdk_response.json")
                
                result_section = response_json.get("result", {})
                
                # 检查所有可能的头像相关字段
                avatar_fields_found = {}
                for key in result_section.keys():
                    key_lower = key.lower()
                    if any(keyword in key_lower for keyword in ['avatar', 'photo', 'image', 'head', 'pic']):
                        value = result_section[key]
                        if isinstance(value, str) and len(value) > 100:
                            avatar_fields_found[key] = f"{value[:50]}... (length: {len(value)})"
                        else:
                            avatar_fields_found[key] = value
                
                print(f"[DEBUG] Avatar-related fields found: {list(avatar_fields_found.keys())}")
                for field, value in avatar_fields_found.items():
                    try:
                        print(f"[DEBUG]   {field}: {value}")
                    except UnicodeEncodeError:
                        print(f"[DEBUG]   {field}: [值包含非ASCII字符，已跳过详细打印]")
                    
                print(f"[DEBUG] Response has avatar_url: {'avatar_url' in result_section}")
                print(f"[DEBUG] Response has avatar_data: {'avatar_data' in result_section}")
                if 'avatar_url' in result_section:
                    try:
                        print(f"[DEBUG] avatar_url value: {result_section['avatar_url'][:100] if result_section['avatar_url'] else 'None'}")
                    except UnicodeEncodeError:
                        print(f"[DEBUG] avatar_url value: [包含非ASCII字符]")
                if 'avatar_data' in result_section:
                    avatar_data_val = result_section['avatar_data']
                    print(f"[DEBUG] avatar_data length: {len(avatar_data_val)}")
                    try:
                        print(f"[DEBUG] avatar_data starts with: {avatar_data_val[:50] if avatar_data_val else 'None'}")
                    except UnicodeEncodeError:
                        print(f"[DEBUG] avatar_data starts with: [包含非ASCII字符]")
                    # 检查是否是完整的 data URI
                    if avatar_data_val.startswith('data:image'):
                        print(f"[DEBUG] [OK] avatar_data is a complete Data URL")
                    else:
                        print(f"[DEBUG] [WARN] avatar_data is NOT a Data URL (may need prefix)")
                    
            except httpx.HTTPStatusError as e:
                raise RuntimeError(f"ResumeSDK API 错误: {e.response.status_code} - {self._safe_str(e.response.text)}")
            except httpx.RequestError as e:
                raise RuntimeError(f"请求 ResumeSDK API 失败: {self._safe_str(e)}")

        # 解析响应
        result = response_json

        # 检查状态码
        status = result.get("status", {})
        if status.get("code") != 200:
            raise RuntimeError(f"ResumeSDK 解析失败: {self._safe_str(status.get('message', '未知错误'))}")

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
