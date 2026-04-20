from __future__ import annotations

# Credibility assessment prompt
CREDIBILITY_ASSESSMENT_PROMPT = """\
You are an expert in behavioral analysis and deception detection.

Question: {question}
Candidate's Answer: {answer}
Resume Context: {resume_context}

Assess the credibility of this answer on the following dimensions:

1. Specificity (0-10):
   - Does the answer include concrete details?
   - Are there specific examples, numbers, or dates?

2. Consistency (0-10):
   - Does it align with resume information?
   - Any contradictions or discrepancies?

3. Confidence Indicators (0-10):
   - Direct, affirmative language
   - Appropriate level of detail
   - Natural speech patterns

4. Relevance (0-10):
   - Does it directly address the question?
   - Is the content appropriate?

Provide:
- overall_score: weighted average (0-100)
- breakdown: scores for each dimension
- indicators: specific observations supporting your assessment
- notes: any additional observations
"""

# Inconsistency detection prompt
INCONSISTENCY_DETECTION_PROMPT = """\
Compare the candidate's answer with their resume to identify inconsistencies.

Resume Information:
{resume_data}

Candidate's Statement:
{statement}

Identify any:
1. Direct contradictions
2. Exaggerations or embellishments
3. Unexplained discrepancies
4. Timeline inconsistencies

For each inconsistency found, provide:
- type: contradiction/exaggeration/discrepancy
- description: what was found
- severity: low/medium/high
"""
