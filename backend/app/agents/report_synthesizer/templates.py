from __future__ import annotations

# Report synthesis prompt
REPORT_SYNTHESIS_PROMPT = """\
You are an expert hiring manager synthesizing an interview evaluation report.

Interview Data:
{interview_data}

Individual Assessments:
{assessments}

Generate a comprehensive evaluation report with:

1. Executive Summary:
   - Brief overview of the candidate
   - Overall impression
   - Key highlights

2. Technical Assessment:
   - Skill verification results
   - Technical depth observed
   - Areas of expertise

3. Behavioral Assessment:
   - Communication skills
   - Problem-solving approach
   - Cultural fit indicators

4. Credibility Analysis:
   - Consistency with resume
   - Confidence in responses
   - Any concerns noted

5. Strengths (3-5 bullet points)

6. Areas for Improvement (2-3 bullet points)

7. Hiring Recommendation:
   - Strong Hire / Hire / Neutral / No Hire
   - Confidence level
   - Rationale

8. Suggested Next Steps:
   - Additional interviews needed
   - Reference check focus areas
   - Onboarding considerations
"""

# Report template (for structured output)
REPORT_TEMPLATE = {
    "candidate_info": {
        "name": "",
        "position": "",
        "interview_date": "",
        "interviewer": "",
    },
    "executive_summary": "",
    "technical_assessment": {
        "score": 0,
        "details": "",
    },
    "behavioral_assessment": {
        "score": 0,
        "details": "",
    },
    "credibility_assessment": {
        "score": 0,
        "details": "",
    },
    "strengths": [],
    "weaknesses": [],
    "recommendation": {
        "decision": "",  # Strong Hire / Hire / Neutral / No Hire
        "confidence": 0,
        "rationale": "",
    },
    "next_steps": [],
}
