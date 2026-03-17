"""OpenAI API integration for derivation explanation with structured output."""

from __future__ import annotations

import json
import os

from openai import OpenAI

from prompts import build_user_prompt
from schemas import DerivationExplanation


def explain_derivation(
    derivation_text: str,
    context_text: str | None = None,
) -> DerivationExplanation:
    """
    Call the OpenAI API to explain a derivation and return a validated structured result.

    Args:
        derivation_text: The derivation excerpt to explain.
        context_text: Optional surrounding context from the paper.

    Returns:
        Parsed and validated DerivationExplanation.

    Raises:
        ValueError: If the API key is missing, the API call fails, or the response
            cannot be parsed into DerivationExplanation.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or not api_key.strip():
        raise ValueError(
            "OPENAI_API_KEY is not set. Add it to a .env file or set the environment variable."
        )

    client = OpenAI(api_key=api_key)
    system_content = (
        "You are a careful mathematical explainer. Output only valid JSON that matches "
        "the following schema. No markdown, no code fences, no extra text.\n\n"
        "Schema: DerivationExplanation with fields: summary (string), steps (array of "
        "{ step_number: int, explanation: string, rule_or_operation: string | null }), "
        "assumptions (array of strings), intuition (string), ambiguities (array of strings), "
        "confidence (one of: \"low\", \"medium\", \"high\")."
    )
    user_content = build_user_prompt(derivation_text, context_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
        )
    except Exception as e:
        err_str = str(e).lower()
        if "429" in err_str or "insufficient_quota" in err_str or "rate limit" in err_str:
            raise ValueError(
                "OpenAI API quota exceeded. Check your plan and billing at "
                "https://platform.openai.com/account/billing and "
                "https://platform.openai.com/docs/guides/error-codes/api-errors."
            ) from e
        raise ValueError(f"API request failed: {e}") from e

    choice = response.choices[0] if response.choices else None
    if not choice or not getattr(choice.message, "content", None):
        raise ValueError("Empty or invalid response from the model.")

    raw_content = choice.message.content.strip()
    # Remove optional markdown code fence
    if raw_content.startswith("```"):
        lines = raw_content.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw_content = "\n".join(lines)

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model output is not valid JSON: {e}") from e

    try:
        return DerivationExplanation.model_validate(data)
    except Exception as e:
        raise ValueError(f"Model output does not match expected schema: {e}") from e
