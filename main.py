from boardSetupClass import Board 
from PlayerClass import Player
from GameLogic import roll_dice
import random
from idp_engine import IDP, model_expand

def setup_game():
    setup_players()
    setup_board()


def setup_players():
    players = [Player("Player 1"), Player("Player 2"), Player("Player 3"), Player("Player 4")]
    # ... set up tiles, resources, players, etc.
    # Determine the initial order based on dice rolls

    # Simulate the initial dice roll to determine the first player
    initial_order = [(player, roll_dice()) for player in players]
    initial_order.sort(key=lambda x: x[1], reverse=True)

    print("Initial Placement Order:")
    for player, roll in initial_order:
        print(f"{player.player_name} rolled a {roll}")

    # Determine the first player based on the highest dice roll
    highest_roll = max(initial_order, key=lambda x: x[1])
    first_player = highest_roll[0]  # The player with the highest roll

    # Find the index of the first player in the list of players
    first_player_index = players.index(first_player)

    # Determine the clockwise order of players
    player_order = players[first_player_index:] + players[:first_player_index]

    # Now, player_order contains the order in which players will take their turns, with the first player going first in a clockwise direction.
    print("First Player:", first_player.player_name)
    print("Player Order:", [player.player_name for player in player_order])


def setup_board():
    board = Board()
    
    kb = IDP.from_file("catan_board_idp_theory.idp")
    T, S = kb.get_blocks("T, S")
    for model in model_expand(T,S, max=1):
        print(model)

    

    # Default Catan layout
    tile_colors = {'hills': '#fa914f', 'forest': '#187b13', 'pasture': '#5ee557', 'mountains': '#9d998f', 'fields': '#fbf250', 'desert': '#fcf799', 'none': 'white'}
    default_tiles = ['mountains', 'pasture', 'forest', 'fields', 'hills', 'pasture', 'hills', 'fields', 'forest', 'desert', 'forest', 'mountains', 'forest', 'mountains', 'fields', 'pasture', 'hills', 'fields', 'pasture']
    default_tokens = [10, 2, 9, 12, 6, 4, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
    tiles = ['none'] * 19
    tokens = [None] * 19
    neg_tiles = [[] for _ in range(19)]
    neg_tokens = [[] for _ in range(19)]
    next_tile = {'none': 'hills', 'hills': 'forest', 'forest': 'mountains', 'mountains': 'fields', 'fields': 'pasture', 'pasture': 'desert', 'desert': 'none'}
    coordinates = [[0, -2], [1, -2], [2, -2], [-1, -1], [0, -1], [1, -1], [2, -1], [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [-2, 1], [-1, 1], [0, 1], [1, 1], [-2, 2], [-1, 2], [0, 2]]
    highlight_tile = None
    extra_constraints = {'centerdesert': False, 'neighbourtoken': False, 'neighbourtile': False, 'balanceprob': False, 'elevenpips': False}

    def reset():
        for i in range(len(tiles)):
            tiles[i] = 'none'
            tokens[i] = None
            neg_tiles[i] = []
            neg_tokens[i] = []

    # Initiating the model expansion and drawing the initial board.
    model_expand()

    print(tiles)

    # board.display_board()
    return board

setup_game()
