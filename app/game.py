#!/usr/bin/env python3
"""Game entrypoint for the Interactive Text Adventure."""
from __future__ import annotations

from engine.actions import describe_current_room, dispatch_command
from engine.io import print_separator
from engine.parser import parse_command
from engine.state import GameState

LAUNCH_HEADING = "TEXT ADVENTURE GAME"


def display_launch_banner() -> None:
    """Print the launch banner as specified in the design document."""
    print_separator()
    print(f"                    {LAUNCH_HEADING}")
    print_separator()
    print()
    print("Welcome to the Text Adventure Game!")
    print("Type 'help' for available commands.")
    print()
    print("Your goal: Reach the Enemy Arena and defeat the enemy!")
    print("------------------------------------------------------------")


def main() -> None:
    """Run the game loop."""
    state = GameState()

    display_launch_banner()
    print()
    describe_current_room(state)

    running = True
    while running and not state.game_over:
        raw = input("> ")
        command = parse_command(raw)
        running = dispatch_command(state, command)


if __name__ == "__main__":
    main()
