"""Static text content for the text adventure game."""
from __future__ import annotations

from engine import world

ROOMS = {
    world.ROOM_START: {
        "name": "Starting Chamber",
        "description": [
            "You are in a dimly lit chamber. Stone walls surround you.",
            "There is a heavy wooden door to the north.",
        ],
        "items": {
            "key": "A rusty key lies on the floor.",
            "note": "A note sits on a dusty table.",
        },
        "exits": "Exits: north",
    },
    world.ROOM_TREASURY: {
        "name": "Treasury Room",
        "description": [
            "You enter a grand treasury room with four ornate archways, each marked with a different symbol: a SWORD (north), a SHIELD (east), a CROWN (west), and a SKULL (south).",
            "Ancient text glows on the wall between them: 'Only courage leads forward.' All archways are open, inviting you to choose.",
        ],
        "items": {
            "inscription": "Ancient text glows faintly on the wall between the archways.",
        },
        "exits": "Archways: north (SWORD), east (SHIELD), west (CROWN), south (SKULL)",
    },
    world.ROOM_ARENA: {
        "name": "Enemy Arena",
        "description": [
            "You enter a circular arena. A menacing enemy stands before you, ready to fight!",
        ],
        "items": {},
        "exits": "Exits: south",
    },
}


def format_note_text(password: str) -> str:
    """Return the note text using the chosen password."""
    return (
        "The note reads: 'The password to unlock the door is: "
        f"{password.upper()}'"
    )


INSCRIPTION_TEXT = (
    "The inscription reads: 'Only courage leads forward. Choose wisely, "
    "for some paths lead backward.'"
)


HELP_TEXT = """========================================
AVAILABLE COMMANDS
========================================

Navigation:
  go north         - Move north
  go south         - Move south
  go east          - Move east (Room 2 only)
  go west          - Move west (Room 2 only)
  look             - Examine current room

Interaction:
  take key / pick up key - Pick up the key
  take note / pick up note - Pick up the note (optional)
  pick up [item]   - Alternative way to take items
  read note / examine note - Read the note
  read inscription / examine inscription - Read wall text (Room 2)
  inventory / i    - Check your items
  unlock door with [password] - Unlock the door
  open door        - Try to open the door

Combat:
  attack           - Attack the enemy

Utility:
  help             - Show available commands
  quit             - Exit game
========================================"""
