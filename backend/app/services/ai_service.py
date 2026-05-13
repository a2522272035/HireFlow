"""
AI service powered by DeepSeek for interview assistance.
"""

from __future__ import annotations

import json
from typing import Any, AsyncGenerator

from app.core.llm import DeepSeekLLM


SYSTEM_ANALYSIS = """你是一位资深招聘专家。请分析候选人简历，从以下维度输出结构化结果：
- 核心优势（3 条以内，聚焦与岗位最匹配的点）
- 潜在风险（2-3 条，如空档期、学历、技能等）
- 建议追问方向（3 条以内）

请以 JSON 格式返回：
{"coreAdvantages": ["..."], "potentialRisks": ["..."], "followUpDirections": ["..."]}
"""

SYSTEM_CHAT = """你是一位专业面试助手，协助面试官对候选人进行结构化面试。
你面前有候选人的简历信息。请根据面试官的提问，结合简历内容给出专业建议或补充信息。
回答应简洁、聚焦、有条理。

格式要求：
- 列表项之间必须空一行（即每个 1. 2. 3. 编号项之间要有空行）
- 段落之间也要空一行
- 使用 Markdown 格式
"""

SYSTEM_GENERATE = """你是一位专业面试官，请根据候选人简历生成 3-5 道高质量面试问题。
问题应涵盖：专业技能、行为面（STAR 法）、候选人简历中的疑点/亮点。
输出格式为有序列表，每道题附一行考察意图说明。
"""


class AIService:
    """AI service for interview-related tasks."""

    def __init__(self) -> None:
        self.llm = DeepSeekLLM()

    async def analyze_resume(
        self,
        resume_data: dict[str, Any],
        profiler_data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Analyze resume and return structured insights."""
        prompt = f"""候选人简历信息：
姓名: {resume_data.get('name', '未知')}
职位: {resume_data.get('position', '未知')}
经验: {resume_data.get('experience', '未知')}年
学历: {resume_data.get('degree', '未知')}
学校: {resume_data.get('school', '未知')}
"""
        if profiler_data:
            highlights = profiler_data.get('highlights', {}).get('items', [])
            risks = profiler_data.get('risks', {}).get('items', [])
            if highlights:
                prompt += f"\n亮点: {'; '.join(str(h) for h in highlights)}"
            if risks:
                prompt += f"\n风险: {'; '.join(str(r) for r in risks)}"

        messages = [
            {"role": "system", "content": SYSTEM_ANALYSIS},
            {"role": "user", "content": prompt},
        ]

        raw = await self.llm.chat(messages, temperature=0.5)

        try:
            start = raw.index("{")
            end = raw.rindex("}") + 1
            return json.loads(raw[start:end])
        except (ValueError, json.JSONDecodeError):
            return {
                "coreAdvantages": ["候选人履历值得关注"],
                "potentialRisks": ["需要进一步沟通确认"],
                "followUpDirections": ["请结合简历深入追问"],
            }

    async def generate_questions(
        self,
        resume_data: dict[str, Any],
    ) -> str:
        """Generate interview questions based on resume."""
        prompt = f"""候选人简历：
姓名: {resume_data.get('name', '未知')}
职位: {resume_data.get('position', '未知')}
经验: {resume_data.get('experience', '未知')}年
技能: {resume_data.get('skills', '未提供')}

请生成面试问题。"""

        messages = [
            {"role": "system", "content": SYSTEM_GENERATE},
            {"role": "user", "content": prompt},
        ]
        return await self.llm.chat(messages, temperature=0.8)

    async def generate_questions_stream(
        self,
        resume_data: dict[str, Any],
    ) -> AsyncGenerator[str, None]:
        """Generate one interview question with streaming output."""
        tags = resume_data.get('tags', [])
        if isinstance(tags, list):
            tags_str = ', '.join(
                tag.get('text', str(tag)) if isinstance(tag, dict) else str(tag)
                for tag in tags
            ) if tags else '未提供'
        else:
            tags_str = '未提供'
        
        work_exps = resume_data.get('work_experiences', [])
        work_exps_str = ''
        if isinstance(work_exps, list) and work_exps:
            for i, job in enumerate(work_exps, 1):
                work_exps_str += f"{i}. {job.get('company', '')} | {job.get('position', '')} | {job.get('duration', '')}\n"
                if job.get('description'):
                    work_exps_str += f"   工作内容: {job.get('description')}\n"
        else:
            work_exps_str = '未提供'
        
        edu_exps = resume_data.get('education_experiences', [])
        edu_exps_str = ''
        if isinstance(edu_exps, list) and edu_exps:
            for i, edu in enumerate(edu_exps, 1):
                edu_exps_str += f"{i}. {edu.get('school', '')} | {edu.get('major', '')} | {edu.get('degree', '')} | {edu.get('duration', '')}\n"
        else:
            edu_exps_str = '未提供'
        
        project_exps = resume_data.get('project_experiences', [])
        project_exps_str = ''
        if isinstance(project_exps, list) and project_exps:
            for i, proj in enumerate(project_exps, 1):
                project_exps_str += f"{i}. {proj.get('name', '')} | {proj.get('role', '')} | {proj.get('duration', '')}\n"
                if proj.get('description'):
                    project_exps_str += f"   项目描述: {proj.get('description')}\n"
        else:
            project_exps_str = '无'
        
        prompt = f"""候选人完整简历信息：

【基本信息】
姓名: {resume_data.get('name', '未知')}
性别: {resume_data.get('gender', '未知')}
年龄: {resume_data.get('age', '未知')}岁
所在城市: {resume_data.get('location', '未知')}
专业: {resume_data.get('major', '未提供')}

【职业信息】
目标职位: {resume_data.get('position', '未知')}
工作年限: {resume_data.get('experience', '未知')}年
期望薪资: {resume_data.get('expected_salary', '未提供')}
目前公司: {resume_data.get('current_company', '未提供')}

【教育经历】
{edu_exps_str}

【工作经历】
{work_exps_str}

【项目经历】
{project_exps_str}

【技能特长】
技能: {resume_data.get('skills', '未提供')}
证书: {resume_data.get('certificates', '未提供')}

【自我评价】
{resume_data.get('self_evaluation', '未提供')}

【联系方式】
邮箱: {resume_data.get('email', '未提供')}
电话: {resume_data.get('phone', '未提供')}

【个人标签】
{tags_str}

请根据以上完整简历信息，生成 1 道有针对性的面试问题。

**必须严格遵守以下输出格式，不要添加任何额外内容：**

1. [问题内容]

考察：[考察意图]

注意：
- "考察："必须在单独的一行
- "1."和"考察："之间必须有且只有一个空行
- 不要输出任何其他文字、解释或说明
- 优先从候选人的工作经历和项目经历中提取问题"""

        messages = [
            {"role": "system", "content": "你是一位专业面试官。请根据候选人的完整简历信息生成恰好1道高质量面试问题。问题应结合候选人的工作经验、空档期、过往工作相关、技能等等其他综合因素之一生成针对性问题，问题需要具体一些。避免学历问题"},
            {"role": "user", "content": prompt},
        ]
        async for chunk in self.llm.chat_stream(messages, temperature=0.8):
            yield chunk

    async def chat(
        self,
        user_message: str,
        chat_history: list[dict[str, str]] | None = None,
        resume_data: dict[str, Any] | None = None,
    ) -> str:
        """Chat with AI assistant about the candidate."""
        messages = [{"role": "system", "content": SYSTEM_CHAT}]

        if resume_data:
            resume_context = (
                f"当前候选人: {resume_data.get('name', '未知')}, "
                f"职位: {resume_data.get('position', '未知')}, "
                f"经验: {resume_data.get('experience', '未知')}年"
            )
            messages.append({"role": "system", "content": resume_context})

        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_message})
        return await self.llm.chat(messages)

    async def chat_stream(
        self,
        user_message: str,
        chat_history: list[dict[str, str]] | None = None,
        resume_data: dict[str, Any] | None = None,
    ) -> AsyncGenerator[str, None]:
        """Chat with AI assistant with streaming response."""
        messages = [{"role": "system", "content": SYSTEM_CHAT}]

        if resume_data:
            work_exps = resume_data.get('work_experiences', [])
            work_exps_str = ''
            if isinstance(work_exps, list) and work_exps:
                for i, job in enumerate(work_exps, 1):
                    work_exps_str += f"{i}. {job.get('company', '')} | {job.get('position', '')} | {job.get('duration', '')}"
                    if job.get('description'):
                        work_exps_str += f"\n   工作内容: {job.get('description')}"
                    work_exps_str += "\n"
            else:
                work_exps_str = '未提供'
            
            edu_exps = resume_data.get('education_experiences', [])
            edu_exps_str = ''
            if isinstance(edu_exps, list) and edu_exps:
                for i, edu in enumerate(edu_exps, 1):
                    edu_exps_str += f"{i}. {edu.get('school', '')} | {edu.get('major', '')} | {edu.get('degree', '')} | {edu.get('duration', '')}\n"
            else:
                edu_exps_str = '未提供'
            
            project_exps = resume_data.get('project_experiences', [])
            project_exps_str = ''
            if isinstance(project_exps, list) and project_exps:
                for i, proj in enumerate(project_exps, 1):
                    project_exps_str += f"{i}. {proj.get('name', '')} | {proj.get('role', '')} | {proj.get('duration', '')}"
                    if proj.get('description'):
                        project_exps_str += f"\n   项目描述: {proj.get('description')}"
                    project_exps_str += "\n"
            else:
                project_exps_str = '无'
            
            resume_context = (
                f"当前候选人完整信息:\n"
                f"姓名: {resume_data.get('name', '未知')}, "
                f"性别: {resume_data.get('gender', '未知')}, "
                f"年龄: {resume_data.get('age', '未知')}岁, "
                f"城市: {resume_data.get('location', '未知')}, "
                f"职位: {resume_data.get('position', '未知')}, "
                f"经验: {resume_data.get('experience', '未知')}年, "
                f"学历: {resume_data.get('degree', '未知')}, "
                f"学校: {resume_data.get('school', '未知')}, "
                f"专业: {resume_data.get('major', '未提供')}, "
                f"期望薪资: {resume_data.get('expected_salary', '未提供')}, "
                f"目前公司: {resume_data.get('current_company', '未提供')}\n"
                f"\n教育经历:\n{edu_exps_str}\n"
                f"工作经历:\n{work_exps_str}\n"
                f"项目经历:\n{project_exps_str}\n"
                f"技能: {resume_data.get('skills', '未提供')}\n"
                f"证书: {resume_data.get('certificates', '未提供')}\n"
                f"自我评价: {resume_data.get('self_evaluation', '未提供')}"
            )
            messages.append({"role": "system", "content": resume_context})

        if chat_history:
            for msg in chat_history:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_message})
        async for chunk in self.llm.chat_stream(messages):
            yield chunk

    async def explain_term(
        self,
        term: str,
        context: str | None = None,
    ) -> dict:
        """
        解释专业名词。优先查本地知识库，找不到则调 AI 并异步写入动态库。

        Returns:
            {"explanation": str, "source": "local" | "ai"}
        """
        from app.services.company_glossary import (
            get_term_explanation,
            async_add_term,
        )

        # 先查本地知识库（预定义 + 动态）
        local = get_term_explanation(term)
        if local:
            return {"explanation": local, "source": "local"}

        # 本地没有，调 AI
        prompt = f"请用简洁易懂的语言解释专业名词「{term}」"
        if context:
            prompt += f"，该词出现在简历中的上下文中：{context}"
        prompt += "。\n要求：\n1. 解释含义（1-2句话）\n2. 说明在工作中的实际应用场景\n3. 控制在100字以内"

        messages = [
            {"role": "system", "content": "你是一位专业的人力资源顾问，擅长用通俗易懂的方式解释简历中的专业术语。"},
            {"role": "user", "content": prompt},
        ]
        ai_result = await self.llm.chat(messages, temperature=0.3)

        # 异步写入动态知识库，不阻塞返回
        if ai_result:
            async_add_term(term, ai_result)

        return {"explanation": ai_result, "source": "ai"}
