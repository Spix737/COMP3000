class Player:
    def __init__(self, name):
        # Initialize a player with a name, resources, settlements, roads, etc.
        self.player_name = name
        self.resources = {
            'wh': 0,
            'wo': 0,
            'or': 0,
            'cl': 0,
            'sh': 0
        }
        pass

        # logic for placing the first 2 settlements
        def place_settlement(self, *board, vertex):
            board[vertex] = self.player_name

        def place_road(self, *board, edge):
            board[edge] = self.player_name
            
        def add_resource(self, resource, qty):
            self.resources[resource] += qty

        def remove_resource(self, resource, qty):
            self.resources[resource] -= qty

