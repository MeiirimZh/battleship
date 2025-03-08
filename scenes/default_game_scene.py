class DefaultGameScene:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.alphabet = 'ABCDEFGHIJ'

        self.offsets = [(0, 0), (1, 1), (1, 0),
                        (1, -1), (0, -1), (-1, -1),
                        (-1, 0), (-1, 1), (0, 1)]
        
        self.building_ships = [([0, 0],), ([0, 0],), ([0, 0],), ([0, 0],),
                        ([0, 0], [0, 1]), ([0, 0], [0, 1]), ([0, 0], [0, 1]),
                        ([0, 0], [0, 1], [0, 2]), ([0, 0], [0, 1], [0, 2]), 
                        ([0, 0], [0, 1], [0, 2], [0, 3])]
        
        self.msg = ""

    def find_ship_orientation(self, ship):
        if len(ship) == 1:
            return "Centered"
        
        if ship[1][0] > ship[0][0]:
            return "Horizontal"
        if ship[1][1] > ship[0][1]:
            return "Vertical"

    def move_ship(self, ship: tuple, direction: str, ship_collection: list):
        """
        Moves given ship depending on the direction value

        Args:
            ship (tuple): tuple containing ship's positions
            direction (str): left, right, up or down
            ship_collection (list): list, where given ship is contained

        Returns:
            void function. Changes the positions of ship
        """

        ship_orientation = self.find_ship_orientation(ship_collection[-1])
        
        if direction == "left":
            if ship_orientation == "Vertical":
                for pos in ship:
                    pos[0] = max(0, pos[0] - 1)
            else:
                if ship[0][0] - 1 >= 0:
                    for pos in ship:
                        pos[0] -= 1
        elif direction == "right":
            if ship_orientation == "Vertical":
                for pos in ship:
                    pos[0] = min(9, pos[0] + 1)
            else:
                if ship[-1][0] + 1 <= 9:
                    for pos in ship:
                        pos[0] += 1
        elif direction == "up":
            if ship_orientation == "Vertical":
                if ship[0][1] - 1 >= 0:
                    for pos in ship:
                        pos[1] -= 1
            else:
                for pos in ship:
                    pos[1] = max(0, pos[1] - 1)
        else:
            if ship_orientation == "Vertical":
                if ship[-1][1] + 1 <= 9:
                    for pos in ship:
                        pos[1] += 1
            else:
                for pos in ship:
                    pos[1] = min(9, pos[1] + 1)
