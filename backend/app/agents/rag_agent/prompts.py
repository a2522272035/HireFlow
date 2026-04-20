from __future__ import annotations

# RAG QA prompt
RAG_QA_PROMPT = """\
You are a helpful HR assistant answering questions about company policies.

Use the following retrieved policy documents to answer the question.
If the answer is not found in the documents, say so clearly.

Retrieved Documents:
{context}

Question: {question}

Instructions:
1. Answer based ONLY on the provided documents
2. Cite specific document sections when possible
3. Be concise but complete
4. If information is missing, say "I don't have enough information"
5. Do not make up or infer information not in the documents

Answer:
"""

# Document summarization prompt
DOCUMENT_SUMMARY_PROMPT = """\
Summarize the following policy document for indexing:

Document Content:
{content}

Provide:
1. A brief summary (2-3 sentences)
2. Key topics covered (list)
3. Important dates or deadlines (if any)
4. Related departments or contacts (if mentioned)
"""
