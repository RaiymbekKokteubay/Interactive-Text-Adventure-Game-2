"""Input parsing utilities for the text adventure game."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ParsedCommand:
    """Represents a normalized player command."""

    verb: str | None
    noun: str | None

    @property
    def is_empty(self) -> bool:
        """Return True when no verb was provided."""
        return not self.verb


def normalize_input(raw: str | None) -> str:
    """Normalize raw user input by trimming and collapsing whitespace."""
    if raw is None:
        return ""
    cleaned = " ".join(raw.strip().split())
    return cleaned.lower()


def parse_command(raw: str | None) -> ParsedCommand:
    """Parse raw input into a verb and optional noun token."""
    normalized = normalize_input(raw)
    if not normalized:
        return ParsedCommand(verb=None, noun=None)
    parts = normalized.split(" ", 1)
    verb = parts[0]
    noun = parts[1] if len(parts) > 1 else None
    return ParsedCommand(verb=verb, noun=noun)
