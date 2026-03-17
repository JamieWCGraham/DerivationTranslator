"""Pydantic models for derivation explanation output."""

from typing import Literal

from pydantic import BaseModel


class DerivationStep(BaseModel):
    """A single step in the derivation explanation."""

    step_number: int
    explanation: str
    rule_or_operation: str | None = None


class DerivationExplanation(BaseModel):
    """Structured explanation of a mathematical derivation."""

    summary: str
    steps: list[DerivationStep]
    assumptions: list[str]
    intuition: str
    ambiguities: list[str]
    confidence: Literal["low", "medium", "high"]
