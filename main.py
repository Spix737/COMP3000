from boardSetupClass import Board 
from PlayerClass import Player
from GameLogic import roll_dice
import random

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
    def place_and_check(i, first = None, second = None, third = None):
        x = True
        # ta = board.terrain_array
        err_count = 0
        unusable = []
        while x == True:
            ptile = random.choice(board.terrain_array)
            if third == None:
                if second == None:
                    if(first == None):
                        board.board[board.tile_types_center[i]] = ptile
                        board.terrain_array.remove(ptile)
                        x = False
                    else:
                        if(ptile in unusable
                            or board.board[board.tile_types_center[i] - first] == ptile):
                            unusable.append(ptile)
                            err_count += 1
                        else:
                            board.board[board.tile_types_center[i]] = ptile
                            board.terrain_array.remove(ptile)
                            x = False
                else:
                    if(ptile in unusable
                        or board.board[board.tile_types_center[i] - first] == ptile
                        or board.board[board.tile_types_center[i] - second] == ptile):
                        err_count += 1
                        unusable.append(ptile)
                    else:
                        board.board[board.tile_types_center[i]] = ptile
                        board.terrain_array.remove(ptile)
                        x = False
            else:
                if(ptile in unusable
                    or board.board[board.tile_types_center[i] - first] == ptile
                    or board.board[board.tile_types_center[i] - second] == ptile
                    or board.board[board.tile_types_center[i] - third] == ptile):
                    unusable.append(ptile)
                    err_count += 1
                else:
                    board.board[board.tile_types_center[i]] = ptile
                    board.terrain_array.remove(ptile)
                    x = False
            if err_count > 20:
                print("Error: too many iterations")
                break

    board = Board()

    # step 1: place hexagons
    # req - ensure adjacent hexagon's aren't of similar type.

    # if (central_desert == True):
        # board.centres.remove(9)
        # board.board[91] = 'X'
    place_and_check(0)
    for i in range(1,3):
        place_and_check(i, 4)
    place_and_check(3, 30)
    for i in range(4,6):
        place_and_check(i, 4, 30, 34)
    place_and_check(6, 4, 34)
    place_and_check(7, 38)
    for i in range(8,11):
        place_and_check(i, 4, 42, 38)
    place_and_check(11, 4, 42)
    place_and_check(12, 42, 38)
    for i in range(13,16):
        place_and_check(i, 4, 42, 38)
    place_and_check(16, 34, 30)
    for i in range(17,19):
        place_and_check(i, 4, 34, 30)

        # if value is equal to either of it's adjacents, select a new value
        # if value is not equal to either of it's adjacents, place value

    # step 2: place number tokens
    # req - ensure adjacent hexagon's don't have the same number token
    # req - tile intersection prob total cannot be higher than 11
    # req - probabilities should be balanced over a resource

    # List of numbers
    numbers = [1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]

    # Define the classes and their instance counts
    class_counts = {'c': 4, 'f': 4, 'm': 4, 'h': 3, 'p': 3}

    # Initialize class objects with empty lists to store assigned numbers
    class_objects = {cls: [] for cls in class_counts}

    # Shuffle the numbers list to distribute them randomly
    random.shuffle(numbers)

    # Distribute numbers as evenly as possible
    while numbers:
        for cls, count in class_counts.items():
            if count > 0:
                # Calculate the current mean for this class
                current_mean = sum(class_objects[cls]) / len(class_objects[cls]) if class_objects[cls] else 0
                # Find the number that minimizes the deviation from the current mean
                number = min(numbers, key=lambda x: abs(current_mean + x - sum(class_objects[cls] + [x]) / (len(class_objects[cls]) + 1)))
                class_objects[cls].append(number)
                numbers.remove(number)
                class_counts[cls] -= 1

    # Print the distribution
    for cls, numbers_assigned in class_objects.items():
        print(f'{cls}: {numbers_assigned}, mean: {sum(numbers_assigned) / len(numbers_assigned)}')
        
    def prob_and_check(i, intersect_a=None, intersect_b=None, intersect_c=None):
        print("prob_and_check")
        # for the provided tile, find the resource type
        resource_type = board.board[board.tile_types_center[i]]
        # LOOP
        x = True
        while x == True:
        # for the resource type, select from the available pip values
            available_numbers_for_resource = class_objects[resource_type]
        # if pip value is valid with the intersects, roll with it
            if intersect_c == None:
                if intersect_b == None:
                    if(intersect_a == None):
                        
                        x = False
                    else:
        # else, go up 
        # LOOP
        # for a pip value, select from the available probabilities
        # if probability is equal to neighbours, don't roll with it

    board.display_board()
    return board

setup_game()
