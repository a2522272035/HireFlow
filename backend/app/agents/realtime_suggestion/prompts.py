from __future__ import annotations

# Real-time suggestion prompt
REALTIME_SUGGESTION_PROMPT = """\
You are an AI interview assistant helping an interviewer in real-time.

Conversation History:
{transcript}

Current Context:
- Position: {position}
- Interview Stage: {stage}
- Topics Covered: {topics}

Based on the conversation, suggest the next action:

1. If the candidate's answer was vague or incomplete:
   - Suggest a specific follow-up question

2. If the candidate mentioned something interesting:
   - Suggest exploring that topic deeper

3. If the interview is going off-track:
   - Suggest bringing it back to key areas

4. If enough information has been gathered on a topic:
   - Suggest moving to the next topic

Provide your suggestion in this format:
- type: follow_up / explore / redirect / move_on
- suggestion: specific action or question
- rationale: brief explanation
"""

# Clarification detection prompt
CLARIFICATION_DETECTION_PROMPT = """\
Analyze the candidate's answer to determine if clarification is needed.

Answer: {answer}

Check for:
1. Vague statements without specifics
2. Jargon without explanation
3. Contradictions or unclear logic
4. Missing context for claims
5. Overly brief responses

Return:
- needs_clarification: true/false
- reason: why clarification is needed
- suggested_clarification: how to ask for clarification
"""
