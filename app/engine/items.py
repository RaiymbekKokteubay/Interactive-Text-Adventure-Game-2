"""Item handling utilities."""
from __future__ import annotations

from typing import Optional, Tuple

from engine.state import GameState
from engine import world

ARTICLES = {"a", "an", "the"}
TAKEABLE_ITEMS = {"key", "note"}


def canonicalize_item(noun: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Return a canonical item name and display label for messaging."""
    if noun is None:
        return None, None
    parts = noun.split()
    while parts and parts[0] in ARTICLES:
        parts.pop(0)
    if not parts:
        return None, None
    cleaned = " ".join(parts)
    if cleaned in TAKEABLE_ITEMS:
        return cleaned, cleaned
    return None, cleaned


def room_has_item(state: GameState, item: str) -> bool:
    """Check whether the current room contains the specified item."""
    return state.room_has_item(state.current_room, item)


def remove_room_item(state: GameState, item: str) -> None:
    """Remove an item from the current room."""
    state.remove_room_item(state.current_room, item)


def reset_room_items(state: GameState) -> None:
    """Reset room items to their starting configuration (unused now)."""
    state.items_in_rooms = {
        world.ROOM_START: {"key", "note"},
        world.ROOM_TREASURY: set(),
        world.ROOM_ARENA: set(),
    }
