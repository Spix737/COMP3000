import random

def decide_int(prompt="Enter an integer: "):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def roll_dice():
    return random.randint(1,6) + random.randint(1,6)

def initial_placements(player_order):
    p_count = len(player_order)
    for i in range(p_count):
        print(f"{player_order[i].player_name}'s turn to place a settlement and road")
        # player_order[i].place_settlement()
        # player_order[i].place_road()
    for i in range(p_count):
        print(f"{player_order[p_count-(i+1)].player_name}'s turn to place a settlement and road")
        # player_order[p_count-i].place_settlement()
        # player_order[p_count-i].place_road()

# player roll -> reward resource
