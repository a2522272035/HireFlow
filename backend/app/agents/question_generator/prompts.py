from __future__ import annotations

# Question generation prompt
QUESTION_GENERATION_PROMPT = """\
You are an expert interviewer preparing questions for a candidate.

Candidate Resume:
{resume_data}

Detected Gaps/Issues:
{gaps}

Generate a comprehensive interview question set including:

1. Technical Questions (3-5):
   - Based on claimed skills and experience
   - Progressive difficulty
   - Practical scenarios

2. Behavioral Questions (2-3):
   - STAR method based
   - Relevant to past experiences

3. Gap-Related Questions (1-2 per gap):
   - Address specific concerns
   - Non-confrontational tone

Format each question with:
- category: technical/behavioral/gap
- question: the question text
- intent: what you're assessing
- follow_ups: potential follow-up questions
"""

# Follow-up question prompt
FOLLOW_UP_PROMPT = """\
Based on the candidate's previous answer:

Previous Answer: {answer}
Original Question: {question}
Context: {context}

Generate a relevant follow-up question to:
1. Probe deeper into vague areas
2. Verify claims made
3. Explore specific details

Return only the follow-up question text.
"""
