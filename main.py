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
                print("Error: too many iterations p&c")
                break
        print("Desert at: ", board.desert_coord)
    board = Board()

    # step 1: place hexagons
    # req - ensure adjacent hexagon's aren't of similar type.

    # if (central_desert == True):
    # board.tile_types_center.remove(91)
    board.board[91] = 'X'
    place_and_check(0)
    for i in range(1,3):
        place_and_check(i, 4)
    place_and_check(3, 30)
    for i in range(4,6):
        place_and_check(i, 4, 30, 34)
    place_and_check(6, 4, 34)
    place_and_check(7, 38)
    # for i in range(8,11):
    place_and_check(8, 4, 42, 38)
    place_and_check(10, 4, 42, 38)
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

    # Create a dictionary with each letter and its corresponding pip values
    resource_pip_dict = {cls: pip_counts_assigned for cls, pip_counts_assigned in resource_pips.items()}

    # Print the distribution
    # for cls, pip_counts_assigned in resource_pips.items():
        # print(f'{cls}: {pip_counts_assigned}, mean: {sum(pip_counts_assigned) / len(pip_counts_assigned)}')
    print(resource_pip_dict)
    
    # function for getting probability from pip
    def pick_pip(given_pip, neighbour_a=0, neighbour_b_d=0, neighbour_c=0):
        x = True
        while x == True:
        # for a pip value, select from the available probabilities
            if neighbour_a != 0:
                if neighbour_b_d != 0:
                    if neighbour_c != 0:
                        if given_pip + neighbour_b_d + neighbour_c <= 11:
                            if given_pip + neighbour_b_d + neighbour_a <= 11:
                                x = False
                                return given_pip
                            else:
                                return -1
                        else:
                            return -1
                    if given_pip + neighbour_b_d + neighbour_a <= 11:
                        x = False
                        return given_pip
                    else:
                        return -1
                else:
                    return given_pip
            else:
                return given_pip

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

    probability_pip_value = {
        0: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        8: 5,
        9: 4,
        10: 3,
        11: 2,
        12: 1,
    }
    
    pip_probability_values = {
        1: [2, 12,],
        2: [3, 3, 11, 11,],
        3: [4, 4, 10, 10,],
        4: [5, 5, 9, 9,],
        5: [6, 6, 8, 8,],
    }

    def pick_probability(i, intersect_a=0, intersect_b=0, intersect_c=0):
        # for the provided tile, find the resource type
        w = True
        while w == True:
            # get the resource type
            tile_resource = board.board[board.tile_types_center[i]]
            if tile_resource == 'X':
                board.board[board.tile_value_left[i]] = 0
                w = False
                break
            # for the resource type, get a pip
            x = True
            our_pips = resource_pip_dict[tile_resource]
            while x == True:
                if len(our_pips) == 0:
                    return "Cornered error - time to try new MAP"
                selected_pip = random.choice(our_pips)
                if intersect_c != 0:
                    possible_pip = pick_pip(selected_pip, probability_pip_value[intersect_a], probability_pip_value[intersect_b], probability_pip_value[intersect_c])
                elif intersect_b != 0:
                    possible_pip = pick_pip(selected_pip, probability_pip_value[intersect_a], probability_pip_value[intersect_b])
                elif intersect_a != 0:
                    possible_pip = pick_pip(selected_pip, probability_pip_value[intersect_a])
                else:
                    possible_pip = pick_pip(selected_pip)
                if possible_pip != -1:
                    resource_pip_dict[tile_resource].remove(selected_pip)
                    x = False
                else:
                    our_pips.remove(selected_pip)

            our_probabilities = pip_probability_values[possible_pip]
            # print(our_probabilities)
            y = True
            while y == True:
                # get a probability using the pip
                possible_probability = random.choice(our_probabilities)
                if intersect_a != 0:
                    if intersect_b != 0:
                        if intersect_c != 0:
                            if intersect_c == possible_probability or intersect_b == possible_probability or intersect_a == possible_probability:
                                # pick a different probability    
                                our_probabilities = [val for val in our_probabilities if val != possible_probability]
                                if len(our_probabilities) == 0:
                                    print("Error: no probs left - time to try new pip")
                                    y = False
                                    break  
                            else:
                                pip_probability_values[possible_pip].remove(possible_probability)
                                board.board[board.tile_value_left[i]] = possible_probability
                                w = False
                                y = False
                                break  
                        if intersect_b == possible_probability or intersect_a == possible_probability:
                            # pick a different probability    
                            our_probabilities = [val for val in our_probabilities if val != possible_probability]
                            if len(our_probabilities) == 0:
                                print("Error: no probs left - time to try new pip")
                                y = False
                                break  
                        else:
                            pip_probability_values[possible_pip].remove(possible_probability)
                            board.board[board.tile_value_left[i]] = possible_probability
                            w = False
                            y = False
                            break  
                    if intersect_a == possible_probability:
                    # pick a different probability    
                        our_probabilities = [val for val in our_probabilities if val != possible_probability]
                        if len(our_probabilities) == 0:
                            print("Error: no probs left - time to try new pip")
                            y = False
                            break  
                    else:
                        pip_probability_values[possible_pip].remove(possible_probability)
                        board.board[board.tile_value_left[i]] = possible_probability
                        w = False
                        y = False
                        break  
                else:
                    pip_probability_values[possible_pip].remove(possible_probability)
                    board.board[board.tile_value_left[i]] = possible_probability
                    w = False
                    y = False
                    break  
            
    def new_map():
        pick_probability(0)
        # print('prob 1 done')
        pick_probability(3)
        # print('prob 4 done')
        a = pick_probability(4, board.board[board.tile_value_left[0]], board.board[board.tile_value_left[3]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 3 done')

        a = pick_probability(1, board.board[board.tile_value_left[4]], board.board[board.tile_value_left[0]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 2 done')
        a = pick_probability(8, board.board[board.tile_value_left[3]], board.board[board.tile_value_left[4]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 9 done')
        a = pick_probability(7, board.board[board.tile_value_left[3]], board.board[board.tile_value_left[8]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 8 done')
        a = pick_probability(12, board.board[board.tile_value_left[7]], board.board[board.tile_value_left[8]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 13 done')
        
        a = pick_probability(5, board.board[board.tile_value_left[1]], board.board[board.tile_value_left[4]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 6 done')
        a = pick_probability(2, board.board[board.tile_value_left[1]], board.board[board.tile_value_left[5]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 5 done')
        a = pick_probability(9, board.board[board.tile_value_left[5]], board.board[board.tile_value_left[4]], board.board[board.tile_value_left[8]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 10 done')
        a = pick_probability(13, board.board[board.tile_value_left[9]], board.board[board.tile_value_left[8]], board.board[board.tile_value_left[12]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 14 done')
        a = pick_probability(16, board.board[board.tile_value_left[12]], board.board[board.tile_value_left[13]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 17 done')

        a = pick_probability(6, board.board[board.tile_value_left[2]], board.board[board.tile_value_left[5]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 7 done')
        a = pick_probability(10, board.board[board.tile_value_left[6]], board.board[board.tile_value_left[5]], board.board[board.tile_value_left[9]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 11 done')
        a = pick_probability(14, board.board[board.tile_value_left[10]], board.board[board.tile_value_left[9]], board.board[board.tile_value_left[13]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 15 done')
        a = pick_probability(17, board.board[board.tile_value_left[14]], board.board[board.tile_value_left[13]], board.board[board.tile_value_left[16]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 18 done')

        a = pick_probability(11, board.board[board.tile_value_left[6]], board.board[board.tile_value_left[10]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        # print('prob 12 done')
        a = pick_probability(15, board.board[board.tile_value_left[11]], board.board[board.tile_value_left[10]], board.board[board.tile_value_left[14]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        print('prob 16 done')
        a = pick_probability(18, board.board[board.tile_value_left[15]], board.board[board.tile_value_left[14]], board.board[board.tile_value_left[17]])
        if a == "Cornered error - time to try new MAP":
            return "Cornered error - time to try new MAP"
        print('prob 19 done')
        board.display_board()

    z = True
    while z == True:
        make = new_map()
        if make != "Cornered error - time to try new MAP":
            z = False

    board.display_board()

        # else, go up 
        # LOOP
        # for a pip value, select from the available probabilities
        # if probability is equal to neighbours, don't roll with it
    board.display_board()
    return board

setup_game()
