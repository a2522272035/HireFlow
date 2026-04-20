from __future__ import annotations

# Resume parsing prompt
RESUME_PARSE_PROMPT = """\
You are an expert resume parser. Extract structured information from the resume.

Resume Content:
{resume_text}

Extract the following information in JSON format:
- personal_info: name, email, phone, location
- skills: list of technical and soft skills
- work_experience: company, title, duration, responsibilities
- education: school, degree, graduation year
- projects: name, description, technologies used
"""

# Gap detection prompt
GAP_DETECTION_PROMPT = """\
You are an expert recruiter analyzing a resume for potential gaps and issues.

Resume Data:
{resume_data}

Identify the following:
1. Employment gaps (periods without work > 3 months)
2. Skill mismatches (claimed vs. demonstrated)
3. Vague descriptions that need clarification
4. Unusual career patterns
5. Missing critical information

For each issue found, provide:
- type: gap_type
- description: brief explanation
- severity: low/medium/high
- suggested_question: follow-up question to ask
"""

# Skill verification prompt
SKILL_VERIFICATION_PROMPT = """\
Given the following skills claimed by a candidate:
{skills}

Generate specific technical questions to verify proficiency level for each skill.
Focus on practical scenarios and real-world applications.
"""
