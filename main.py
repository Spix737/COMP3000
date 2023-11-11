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
            if ptile == 'X':
                board.desert_coord = board.tile_types_center[i]
                board.board[board.tile_types_center[i]] = ptile
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
        print("Desert at: ", board.desert_coord)
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
    pip_counts = [1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]

    # Define the classes and their instance counts
    resource_counts = {'c': 4, 'f': 4, 'm': 4, 'h': 3, 'p': 3}

    # Initialize resource objects with empty lists to store assigned numbers
    resource_pips = {cls: [] for cls in resource_counts}

    # Shuffle the numbers list to distribute them randomly
    random.shuffle(pip_counts)

    # Distribute pip_counts as evenly as possible
    while pip_counts:
        for cls, count in resource_counts.items():
            if count > 0:
                # Calculate the current mean for this resource
                current_mean = sum(resource_pips[cls]) / len(resource_pips[cls]) if resource_pips[cls] else 0
                # Find the number that minimizes the deviation from the current mean
                pip = min(pip_counts, key=lambda x: abs(current_mean + x - sum(resource_pips[cls] + [x]) / (len(resource_pips[cls]) + 1)))
                resource_pips[cls].append(pip)
                pip_counts.remove(pip)
                resource_counts[cls] -= 1

    # Print the distribution
    for cls, pip_counts_assigned in resource_pips.items():
        print(f'{cls}: {pip_counts_assigned}, mean: {sum(pip_counts_assigned) / len(pip_counts_assigned)}')
    

    # function for getting probability from pip
    def pick_pip(available_pips, neighbour_a=0, neighbour_b_d=0, neighbour_c=0):
        x = True
        while x == True:
        # for a pip value, select from the available probabilities
            our_pips = available_pips
            selected_pip =  random.choice(our_pips)
            if neighbour_a != 0:
                if neighbour_b_d != 0:
                    if neighbour_c != 0:
                        if selected_pip + neighbour_b_d + neighbour_c <= 11:
                            if selected_pip + neighbour_b_d + neighbour_a <= 11:
                                available_pips.remove(selected_pip)
                                return selected_pip, available_pips
                            else:
                                our_pips.remove(selected_pip)
                                if len(our_pips) == 0:
                                    print("Error: no pips left")
                                    break
                    if selected_pip + neighbour_b_d + neighbour_a <= 11:
                                available_pips.remove(selected_pip)
                                return selected_pip, available_pips
                    else:
                        our_pips.remove(selected_pip)
                        if len(our_pips) == 0:
                            print("Error: no pips left")
                            break
            else:
                available_pips.remove(selected_pip)
                return selected_pip, available_pips


# pick a pip
# max amount of neighbours = 3
# is the pip total among neighbours > 11?
# if yes, pick again
# if no, return the pip

# using pip, pick a probability
# max amount of neighbours = 3
# is the probability different to either neighbour?
# if yes, return the probability
# if no, pick again - but not that probability
# if no probabilities, pick another pip but not that pip

    def pick_probability(i, intersect_a=None, intersect_b=None, intersect_c=None):
        pip_probability_values = {
            1: [2, 12,],
            2: [3, 3, 11, 11,],
            3: [4, 4, 10, 10,],
            4: [5, 5, 9, 9,],
            5: [6, 6, 8, 8,],
        }
        # for the provided tile, find the resource type
        resource_type = board.board[board.tile_types_center[i]]
        # LOOP
        x = True
        while x == True:
        # for the resource type, get a pip
            selected_pip = pick_pip(pip_counts_assigned[resource_type] )

        # else, go up 
        # LOOP
        # for a pip value, select from the available probabilities
        # if probability is equal to neighbours, don't roll with it

    board.display_board()
    return board

setup_game()
