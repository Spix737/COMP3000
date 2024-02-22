class Player:
    def __init__(self, name):
        # Initialize a player with a name, resources, settlements, roads, etc.
        self.player_name = name
        self.resources = {
            'wheat': 0,
            'wood': 0,
            'ore': 0,
            'clay': 0,
            'sheep': 0
        }
        self.trades = {
            'wheat': 4,
            'wood': 4,
            'ore': 4,
            'clay': 4,
            'sheep': 4
        }

        # logic for placing the first 2 settlements
        def place_settlement(self, board, vertex):
            decide_int()
            board[vertex] = self.player_name

        def place_road(self, board, edge):
            board[edge] = self.player_name
            
        def add_resource(self, resource, qty):
            self.resources[resource] += qty

        def remove_resource(self, resource, qty):
            self.resources[resource] -= qty


        def decide_int(prompt="Enter an integer: "):
            while True:
                try:
                    user_input = int(input(prompt))
                    return user_input
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")
