import math
import re
import random
from boardSetupClass import Board
from PlayerClass import Player
from GameLogic import roll_dice, initial_placements
from idp_engine import IDP, model_expand

def play_game():
    '''set up a instance of a game'''
    player_order = setup_players()
    board = setup_board()
    initial_placements(player_order)

    board.board[2] = 'p1'
    board.board[28] = 'P1'
    board.board[70] = 'p1'
    board.board[176] = 'P1'
    board.board[60] = 'P1'
    pe1 = Player("P1")
    board.display_board()

    resource_per_roll(board, pe1, 6)
    resource_per_roll(board, pe1, 8)
    # game loop
    # gameRunning = True
    # while gameRunning:
    #     for player in player_order:

    #         action = select_action(get_state())

    #         # game.play_turn(action)


    # given map, current available build positions,

    # allow use of dev card (once per turn)
    #
    # roll dice
    #   if digit, hand out cards
    #   if 7, discard, then move robber
    #     if 2+ players on tile's vertices, pick a player & steal card, else steal card (if player has a card)
    #   if unused, allow use of dev card
    #

    # build - trade cycle
    # while endTurn flag is not set
    #   allow to trade (if resources are available, then remove from inventory)
    #   Trading:
    #   
    #   allow to build (if resources are available, then remove from inventory)


def setup_players():
    '''set up the players for the game'''
    players = [Player("P1"), Player("P2"), Player("P3"), Player("P4")]
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
    return player_order


def setup_board():
    '''set up the board for a game'''
    board = Board()
    # default_tiles = ['mountains', 'pasture', 'forest', 'fields', 'hills', 'pasture', 'hills', 'fields', 'forest', 'desert', 'forest', 'mountains', 'forest', 'mountains', 'fields', 'pasture', 'hills', 'fields', 'pasture']
    # default_tokens = [10, 2, 9, 12, 6, 4, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
    tiles = ['none'] * 19
    tokens = [None] * 19
    neg_tiles = [[] for _ in range(19)]
    neg_tokens = [[] for _ in range(19)]
    next_tile = {'none': 'hills', 'hills': 'forest', 'forest': 'mountains', 'mountains': 'fields', 'fields': 'pasture', 'pasture': 'desert', 'desert': 'none'}
    # coordinates = [[0, -2], [1, -2], [2, -2], [-1, -1], [0, -1], [1, -1], [2, -1], [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [-2, 1], [-1, 1], [0, 1], [1, 1], [-2, 2], [-1, 2], [0, 2]]
    extra_constraints = {'centerdesert': False, 'neighbourtoken': True, 'neighbourtile': True, 'balanceprob': True, 'elevenpips': True}

    kb = IDP.from_file("catan_board_idp_theory.idp")

    # add limitations to 

    T, S = kb.get_blocks("T, S")
    for model in model_expand(T,S, max=1):
        # print(model)

        # Split the model into categories
        categories = re.split(r"(\w+ := .+?})", model)
        del categories[0]     
        tile_type = categories[0]
        tile_token = categories[2]
        pattern = r"\((-?\d+), (-?\d+)\) -> (\w+)"
        # Create a dictionary to store the results
        matches = re.findall(pattern, tile_type)
        coordinate_tile_dict = {(int(x), int(y)): tile_type for x, y, tile_type in matches}
        matches = re.findall(pattern, tile_token)
        coordinate_token_dict = {(int(x), int(y)): tile_token for x, y, tile_token in matches}

        # Print the results
        for coordinates, tile_type in coordinate_tile_dict.items():
            q = coordinates[0]
            r = coordinates[1]
            idx = axialCoordToTileId(q, r)
            if idx is not None:
              tiles[idx] = tile_type
        for coordinates, tile_token in coordinate_token_dict.items():
            q = coordinates[0]
            r = coordinates[1]
            idx = axialCoordToTileId(q, r)
            if idx is not None:
              tokens[idx] = tile_token

    for i in range(0,len(tiles)):
        index = board.tile_value_left[i]
        board.board[index] = tokens[i]
        board.board[index+1] = tiles[i]
    # print('tiles:')
    # print(tiles)
    # print('tokens:')
    # print(tokens)
    board.display_board()
    return board

# ADD THIS INFO TO OUR ARRAY

def axialCoordToTileId(q, r):
    '''Converts axial coordinates to a tile id'''
    # If invalid, return null.
    if abs(q + r) > 2:
        return None
    idx = None
    if (r == -2):
        idx = abs(q)
    elif (r == -1): 
        idx = q + 4
    elif (r == 0): 
        idx = q + 9
    elif (r == 1): 
        idx = q + 14
    elif (r == 2): 
        idx = q + 18
    return idx

def setNeg(negDict, neg_tiles, neg_tokens):
#   for i in negDict['tile_type']:
#     coords = i
#     coords = coords.replace(')', '').replace('(', '').replace("'", '')
#     coords = coords.split(', ')
#     q = int(coords[0])
#     r = int(coords[1])
#     idx = axialCoordToTileId(q, r)
#     neg_tiles[idx] = int(negDict['tile_type'][i])
#     # console.log(negDict['tile_token'])
#   for j in negDict['tile_token']:
#     coords = j
#     coords = coords.replace(')', '').replace('(', '').replace("'", '')
#     coords = coords.split(', ')
#     q = int(coords[0])
#     r = int(coords[1])
#     idx = axialCoordToTileId(q, r)
#     neg_tokens[idx] = int(negDict['tile_token'][i])

# def setPos(posDict, tiles, tokens):
#   for i in posDict['tile_type']:
#     coords = i
#     coords = coords.replace(')', '').replace('(', '').replace("'", '')
#     coords = coords.split(', ')
#     q = int(coords[0])
#     r = int(coords[1])
#     idx = axialCoordToTileId(q, r)
#     if idx == None:
#       continue
#     tiles[idx] = posDict['tile_type'][i]
#     # console.log(posDict['tile_token'])
#   for j in posDict['tile_token']:
#     coords = j
#     coords = coords.replace(')', '').replace('(', '').replace("'", '')
#     coords = coords.split(', ')
#     q = int(coords[0])
#     r = int(coords[1])
#     idx = axialCoordToTileId(q, r)
#     if idx == None:
#       continue
#     tokens[idx] = int(posDict['tile_token'][i])
    print('does nothing')

def reset(tiles, tokens):
    '''resets the board'''
    for i in range(len(tiles)):
        tiles[i] = 'none'
        tokens[i] = None
        # neg_tiles[i] = []
        # neg_tokens[i] = []

    # board.display_board()

def select_action():
    '''selects an action for an AI player'''
    print('does nothing')

def select_action_human():
    '''selects an action for a human player'''
    print('does nothing')

def get_state():
    '''returns the state of the game'''
    # what data will be needed for the AI:
        
    # needs to return the map, the players & each of their resources but NOT their dev cards
    # Check whether MANUAL % calculation of resource probs, r. probs per player, etc is needed or if done my ml.
    
    print('does nothing')

#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
#  NEED TO DETERMINE METHOD TO NAVIGATE THROUGH HEXES IN A CORRECT FASHION
def resource_per_roll(board, player, roll_no):
    # returns the resources
    resources = {
        'wheat': 0,
        'wood': 0,
        'ore': 0,
        'clay': 0,
        'sheep': 0
    }
    print('roll_no: ' + str(roll_no))
    hex_id = 1
    for val in board.tile_value_left:
        print('val: ' + str(val))
        print('board.board[val]: ' + str(board.board[val]))
        if board.board[val] == str(roll_no):
            print('roll_no: ' + str(roll_no))
            increment = 4 * hex_id
            print('increment/4: ' + str(increment/4))
            for i in board.first_hex_vertices:
                if board.board[i + increment] == player.player_name.lower():
                    print("board.board[c]: " + str(board.tile_types_center[hex_id]))
                    print("board.resource_tile_map: " + str(board.resource_tile_map[board.tile_types_center[hex_id]]))
                    resources[board.resource_tile_map[board.tile_types_center[hex_id]]] += 1

                elif board.board[i + increment] == player.player_name.upper():
                    print("board.board[c]: " + str(board.tile_types_center[hex_id]))
                    # print("board.resource_tile_map: " + str(board.resource_tile_map[board.board[7 + increment]]))
                    resources[board.resource_tile_map[board.tile_types_center[hex_id]]] += 2
        hex_id += 0

    print(resources)
    return resources




play_game()