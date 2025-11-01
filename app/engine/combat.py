"""Combat mechanics for the text adventure game."""
from __future__ import annotations

import random

from engine.state import GameState

COMBAT_BANNER_WIDTH = 40


def _print_banner_line(title: str) -> None:
    """Print a banner consisting of separator/title/separator."""
    print("=" * COMBAT_BANNER_WIDTH)
    print(title)
    print("=" * COMBAT_BANNER_WIDTH)


def start_combat(state: GameState) -> None:
    """Initialize combat state and show the opening banner."""
    state.in_combat = True
    state.enemy_hp = 10
    # Ensure the player health reflects the starting maximum.
    if state.player_hp > 20:
        state.player_hp = 20

    _print_banner_line("COMBAT BEGINS!")
    print(f"Enemy Health: {state.enemy_hp}/10")
    print(f"Your Health: {state.player_hp}/20")
    print()
    print("Type 'attack' to fight!")


def _handle_victory(state: GameState) -> None:
    """Print victory banner and end the game."""
    _print_banner_line("VICTORY!")
    print("You defeated the enemy! You win!")
    print("Congratulations on completing the adventure!")
    print("=" * COMBAT_BANNER_WIDTH)
    state.in_combat = False
    state.game_over = True


def _handle_defeat(state: GameState) -> None:
    """Print defeat banner and end the game."""
    _print_banner_line("DEFEAT!")
    print("You have been defeated. Game Over.")
    print("Better luck next time!")
    print("=" * COMBAT_BANNER_WIDTH)
    state.in_combat = False
    state.game_over = True


def perform_attack_round(state: GameState) -> bool:
    """Execute one round of combat.

    Returns True if combat continues, False if the game should end.
    """
    if not state.in_combat:
        print("There's nothing to attack here.")
        return True

    player_damage = random.randint(1, 6)
    state.enemy_hp = max(0, state.enemy_hp - player_damage)
    print(f"You attack for {player_damage} damage!")
    print(f"Enemy Health: {state.enemy_hp}/10")

    if state.enemy_hp <= 0:
        _handle_victory(state)
        return False

    enemy_damage = random.randint(1, 4)
    state.player_hp = max(0, state.player_hp - enemy_damage)
    print(f"Enemy attacks for {enemy_damage} damage!")
    print(f"Your Health: {state.player_hp}/20")

    if state.player_hp <= 0:
        _handle_defeat(state)
        return False

    return True
