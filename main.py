from boardSetupClass import Board 
from PlayerClass import Player
from GameLogic import roll_dice

def setup_game():
    board = Board()
    players = [Player("Player 1"), Player("Player 2"), Player("Player 3"), Player("Player 4")]
    # ... set up tiles, resources, players, etc.

    # Determine the initial order based on dice rolls
    initial_order = [(player, roll_dice()) for player in players]
    initial_order.sort(key=lambda x: x[1], reverse=True)

    print("Initial Placement Order:")
    for player, roll in initial_order:
        print(f"{player.player_name} rolled a {roll}")

    for player, roll in initial_order:
        print(f"{player.player_name}'s turn to place a settlement.")
        # Implement logic for allowing the player to place a settlement

    for player, roll in reversed(initial_order):
        print(f"{player.player_name}'s turn to place a settlement.")
        # Implement logic for allowing the player to place a settlement

setup_game()
