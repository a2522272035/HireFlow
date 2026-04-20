from __future__ import annotations

import tiktoken


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens in text for specified model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))


def truncate_to_token_limit(
    text: str,
    max_tokens: int,
    model: str = "gpt-4",
) -> str:
    """Truncate text to fit within token limit."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text

    truncated_tokens = tokens[:max_tokens]
    return encoding.decode(truncated_tokens)


def estimate_cost(tokens: int, model: str = "gpt-4") -> float:
    """Estimate API cost based on token count."""
    # Pricing per 1K tokens (approximate, update as needed)
    pricing = {
        "gpt-4": 0.03,
        "gpt-4-turbo": 0.01,
        "gpt-3.5-turbo": 0.0015,
    }

    rate = pricing.get(model, 0.03)
    return (tokens / 1000) * rate
