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

    def find_ship_orientation(self, ship: tuple):
        """
        Finds given ship's orientation

        Args:
            ship (tuple): tuple containing ship's positions

        Returns:
            str: ship's orientation: 'Centered', 'Vertical' or 'Horizontal'
        """
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

        if ship_orientation == "Horizontal":
            width = len(ship)
            height = 1
        else:
            width = 1
            height = len(ship)
        
        if direction == "left":
            if ship[0][0] > 0:
                for pos in ship:
                    pos[0] -= 1
        elif direction == "up":
            if ship[0][1] > 0:
                for pos in ship:
                    pos[1] -= 1
        elif direction == "right":
            if ship[0][0] + width != 10:
                for pos in ship:
                    pos[0] += 1
        else:
            if ship[0][1] + height != 10:
                for pos in ship:
                    pos[1] += 1
