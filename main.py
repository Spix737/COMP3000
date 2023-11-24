import math
import re
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
    # default_tiles = ['mountains', 'pasture', 'forest', 'fields', 'hills', 'pasture', 'hills', 'fields', 'forest', 'desert', 'forest', 'mountains', 'forest', 'mountains', 'fields', 'pasture', 'hills', 'fields', 'pasture']
    # default_tokens = [10, 2, 9, 12, 6, 4, 10, 9, 11, 7, 3, 8, 8, 3, 4, 5, 5, 6, 11]
    tiles = ['none'] * 19
    tokens = [None] * 19
    neg_tiles = [[] for _ in range(19)]
    neg_tokens = [[] for _ in range(19)]
    next_tile = {'none': 'hills', 'hills': 'forest', 'forest': 'mountains', 'mountains': 'fields', 'fields': 'pasture', 'pasture': 'desert', 'desert': 'none'}
    # coordinates = [[0, -2], [1, -2], [2, -2], [-1, -1], [0, -1], [1, -1], [2, -1], [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [-2, 1], [-1, 1], [0, 1], [1, 1], [-2, 2], [-1, 2], [0, 2]]
    extra_constraints = {'centerdesert': False, 'neighbourtoken': False, 'neighbourtile': False, 'balanceprob': False, 'elevenpips': False}

    kb = IDP.from_file("catan_board_idp_theory.idp")
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
            if idx != None:
              tiles[idx] = tile_type
        for coordinates, tile_token in coordinate_token_dict.items():
            q = coordinates[0]
            r = coordinates[1]
            idx = axialCoordToTileId(q, r)
            if idx != None:
              tokens[idx] = tile_token

    print('tiles:')
    print(tiles)
    print('tokens:')
    print(tokens)

# ADD THIS INFO TO OUR ARRAY

def axialCoordToTileId(q, r):
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
  for i in negDict['tile_type']:
    coords = i
    coords = coords.replace(')', '').replace('(', '').replace("'", '')
    coords = coords.split(', ')
    q = int(coords[0])
    r = int(coords[1])
    idx = axialCoordToTileId(q, r)
    neg_tiles[idx] = int(negDict['tile_type'][i])
    # console.log(negDict['tile_token'])
  for j in negDict['tile_token']:
    coords = j
    coords = coords.replace(')', '').replace('(', '').replace("'", '')
    coords = coords.split(', ')
    q = int(coords[0])
    r = int(coords[1])
    idx = axialCoordToTileId(q, r)
    neg_tokens[idx] = int(negDict['tile_token'][i])

def setPos(posDict, tiles, tokens):
  for i in posDict['tile_type']:
    coords = i
    coords = coords.replace(')', '').replace('(', '').replace("'", '')
    coords = coords.split(', ')
    q = int(coords[0])
    r = int(coords[1])
    idx = axialCoordToTileId(q, r)
    if idx == None:
      continue
    tiles[idx] = posDict['tile_type'][i]
    # console.log(posDict['tile_token'])
  for j in posDict['tile_token']:
    coords = j
    coords = coords.replace(')', '').replace('(', '').replace("'", '')
    coords = coords.split(', ')
    q = int(coords[0])
    r = int(coords[1])
    idx = axialCoordToTileId(q, r)
    if idx == None:
      continue
    tokens[idx] = int(posDict['tile_token'][i])

  def reset(neg_tiles, neg_tokens):
      for i in range(len(tiles)):
          tiles[i] = 'none'
          tokens[i] = None
          neg_tiles[i] = []
          neg_tokens[i] = []

    # board.display_board()


setup_game()
