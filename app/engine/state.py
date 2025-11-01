"""Game state management for the text adventure game."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Set

from engine import world

PASSWORD_OPTIONS = ["shadow", "raiymbek", "valor", "courage"]


@dataclass
class GameState:
    """Represents the mutable state of the game session."""

    current_room: str = world.ROOM_START
    player_hp: int = 20
    enemy_hp: int = 10
    inventory: List[str] = field(default_factory=list)
    items_in_rooms: Dict[str, Set[str]] = field(
        default_factory=lambda: {
            world.ROOM_START: {"key", "note"},
            world.ROOM_TREASURY: set(),
            world.ROOM_ARENA: set(),
        }
    )
    door_locked: bool = True
    in_combat: bool = False
    game_over: bool = False
    door_password: str = field(default_factory=lambda: random.choice(PASSWORD_OPTIONS))

    def has_item(self, item: str) -> bool:
        """Return True if the player currently holds the given item."""
        return item in self.inventory

    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory if not already present."""
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_room_item(self, room_id: str, item: str) -> None:
        """Remove an item from the specified room."""
        room_items = self.items_in_rooms.get(room_id)
        if room_items and item in room_items:
            room_items.remove(item)

    def room_has_item(self, room_id: str, item: str) -> bool:
        """Return True when a room still contains the specified item."""
        return item in self.items_in_rooms.get(room_id, set())
