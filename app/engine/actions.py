"""Command handling for the text adventure game."""
from __future__ import annotations

from engine.parser import ParsedCommand
from engine.state import GameState
from engine import combat, items, world
from engine.io import print_room_title
from data import text as text_module

CARDINAL_DIRECTIONS = {"north", "south", "east", "west"}


def describe_current_room(state: GameState) -> None:
    """Display the description of the player's current location."""
    room_def = text_module.ROOMS[state.current_room]
    print_room_title(room_def["name"])
    for line in room_def["description"]:
        print(line)

    for item_key, item_text in room_def["items"].items():
        if item_key in items.TAKEABLE_ITEMS:
            if items.room_has_item(state, item_key):
                print(item_text)
        else:
            print(item_text)

    print(room_def["exits"])


def show_inventory(state: GameState) -> None:
    """Print the player's current inventory."""
    if not state.inventory:
        print("Your inventory is empty.")
        return

    print("You are carrying:")
    for entry in state.inventory:
        print(f"  - {entry}")


def handle_take(state: GameState, noun: str | None, verb_label: str = "take") -> None:
    """Handle taking or picking up an item."""
    canonical, cleaned = items.canonicalize_item(noun)

    if canonical is None:
        if noun is None or cleaned is None:
            print(f"What do you want to {verb_label}?")
            return
        print(f"There's no {cleaned} here.")
        return

    if not items.room_has_item(state, canonical):
        print(f"There's no {canonical} here.")
        return

    items.remove_room_item(state, canonical)
    state.add_item(canonical)
    print(f"You take the {canonical}.")


def handle_read(state: GameState, noun: str | None) -> None:
    """Handle reading readable items."""
    if noun is None:
        print("What do you want to read?")
        return

    cleaned = noun.strip()
    if cleaned.startswith("the "):
        cleaned = cleaned[4:]

    if cleaned == "note":
        if items.room_has_item(state, "note") or state.has_item("note"):
            print(text_module.format_note_text(state.door_password))
        else:
            print("There's no note here.")
        return

    if cleaned == "inscription":
        if state.current_room == world.ROOM_TREASURY:
            print(text_module.INSCRIPTION_TEXT)
        else:
            print("There's no inscription here.")
        return

    print(f"There's no {cleaned} here.")


def handle_open_door(state: GameState) -> None:
    """Handle the open door command."""
    if state.current_room == world.ROOM_START:
        if state.door_locked:
            print("The door is locked.")
        else:
            print("The door is already unlocked. Use 'go north' to pass through.")
        return

    if state.current_room == world.ROOM_TREASURY:
        print("The archways here are always open. Use 'go [direction]' to move through them.")
        return

    print("There's no door to open here.")


def handle_unlock_door(state: GameState, noun: str | None) -> None:
    """Handle unlocking the door with a password."""
    if state.current_room != world.ROOM_START:
        print("There's no door to unlock here.")
        return

    if not state.door_locked:
        print("The door is already unlocked.")
        return

    if not state.has_item("key"):
        print("You don't have a key.")
        return

    if noun is None:
        print("The password is incorrect.")
        return

    cleaned = noun.strip()
    if cleaned.startswith("door "):
        cleaned = cleaned[5:]

    if cleaned.startswith("with "):
        cleaned = cleaned[5:]
    elif cleaned.startswith("door with "):
        cleaned = cleaned[10:]

    if "door with " in noun:
        password = noun.split("door with ", 1)[1].strip()
    elif cleaned:
        password = cleaned
    else:
        password = ""

    if not password:
        print("The password is incorrect.")
        return

    if password.lower() != state.door_password:
        print("The password is incorrect.")
        return

    state.door_locked = False
    print("The door unlocks with a click!")


def handle_go(state: GameState, noun: str | None) -> None:
    """Handle movement commands."""
    if noun is None:
        print("What direction do you want to go?")
        return

    direction = noun.strip().lower()
    if direction not in CARDINAL_DIRECTIONS:
        print(f"You can't go {direction} from here.")
        return

    if state.current_room == world.ROOM_START:
        if direction == "north":
            if state.door_locked:
                print("The door is locked.")
            else:
                state.current_room = world.ROOM_TREASURY
                describe_current_room(state)
            return
        print(f"You can't go {direction} from here.")
        return

    if state.current_room == world.ROOM_TREASURY:
        if direction == "north":
            state.current_room = world.ROOM_ARENA
            describe_current_room(state)
            if not state.in_combat and not state.game_over:
                combat.start_combat(state)
            return
        if direction == "south":
            state.current_room = world.ROOM_START
            describe_current_room(state)
            return
        if direction == "east":
            print("You feel a strange force pull you back...")
            state.current_room = world.ROOM_START
            describe_current_room(state)
            return
        if direction == "west":
            print("A magical barrier repels you!")
            state.current_room = world.ROOM_START
            describe_current_room(state)
            return
        print(f"You can't go {direction} from here.")
        return

    if state.current_room == world.ROOM_ARENA:
        if direction == "south":
            if state.in_combat:
                print("You can only 'attack' during combat!")
                return
            state.current_room = world.ROOM_TREASURY
            describe_current_room(state)
            return
        print(f"You can't go {direction} from here.")
        return

    room = world.get_room(state.current_room)
    destination = room.exits.get(direction)
    if destination is None:
        print(f"You can't go {direction} from here.")
        return

    state.current_room = destination
    describe_current_room(state)


def dispatch_command(state: GameState, command: ParsedCommand) -> bool:
    """Route a parsed command to its handler. Returns False to exit the game."""
    if state.in_combat:
        if command.is_empty:
            print("You can only 'attack' during combat!")
            return True
        verb = command.verb or ""
        if verb == "quit":
            print("Goodbye!")
            return False
        if verb == "attack":
            return combat.perform_attack_round(state)
        print("You can only 'attack' during combat!")
        return True

    if command.is_empty:
        print("I don't understand that command. Type 'help' for available commands.")
        return True

    verb = command.verb or ""
    noun = command.noun

    if verb == "help":
        print(text_module.HELP_TEXT)
        return True

    if verb == "quit":
        print("Goodbye!")
        return False

    if verb == "look":
        describe_current_room(state)
        return True

    if verb in {"inventory", "i"}:
        show_inventory(state)
        return True

    if verb == "take":
        handle_take(state, noun, verb_label="take")
        return True

    if verb == "pick":
        if noun is None:
            print("What do you want to pick up?")
            return True
        if noun.startswith("up "):
            remaining = noun[3:]
            handle_take(state, remaining, verb_label="pick up")
            return True
        if noun == "up":
            print("What do you want to pick up?")
            return True
        handle_take(state, noun, verb_label="pick")
        return True

    if verb in {"read", "examine"}:
        handle_read(state, noun)
        return True

    if verb == "open":
        if noun is None:
            print("What do you want to open?")
            return True
        if noun.strip() == "door":
            handle_open_door(state)
        else:
            print("There's nothing like that to open.")
        return True

    if verb == "unlock":
        handle_unlock_door(state, noun)
        return True

    if verb == "go":
        handle_go(state, noun)
        return True

    if verb in CARDINAL_DIRECTIONS:
        handle_go(state, verb)
        return True

    if verb == "attack":
        print("There's nothing to attack here.")
        return True

    print("I don't understand that command. Type 'help' for available commands.")
    return True
