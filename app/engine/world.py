"""World layout and room definitions for the text adventure game."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

ROOM_START = "room1"
ROOM_TREASURY = "room2"
ROOM_ARENA = "room3"


@dataclass(frozen=True)
class Room:
    """Represents a room within the game world."""

    id: str
    name: str
    exits: Dict[str, str]


ROOMS: Dict[str, Room] = {
    ROOM_START: Room(
        id=ROOM_START,
        name="Starting Chamber",
        exits={"north": ROOM_TREASURY},
    ),
    ROOM_TREASURY: Room(
        id=ROOM_TREASURY,
        name="Treasury Room",
        exits={
            "north": ROOM_ARENA,
            "east": ROOM_START,  # Trap logic to be refined later
            "west": ROOM_START,  # Trap logic to be refined later
            "south": ROOM_START,
        },
    ),
    ROOM_ARENA: Room(
        id=ROOM_ARENA,
        name="Enemy Arena",
        exits={"south": ROOM_TREASURY},
    ),
}


def get_room(room_id: str) -> Room:
    """Retrieve the room definition for the given identifier."""
    return ROOMS[room_id]
