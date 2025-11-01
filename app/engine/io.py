"""Output formatting helpers for the text adventure game."""
from __future__ import annotations

SEPARATOR_WIDTH = 60


def print_separator(char: str = "=", width: int = SEPARATOR_WIDTH) -> None:
    """Print a repeated character line used as a separator."""
    print(char * width)


def print_room_title(title: str) -> None:
    """Print a room title followed by an underline of matching length."""
    print(title)
    print("-" * len(title))
