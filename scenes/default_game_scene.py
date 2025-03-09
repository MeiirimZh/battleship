class DefaultGameScene:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.alphabet = 'ABCDEFGHIJ'

        self.offsets = [(0, 0), (1, 1), (1, 0),
                        (1, -1), (0, -1), (-1, -1),
                        (-1, 0), (-1, 1), (0, 1)]
        
        self.building_ships = [[[0, 0],], [[0, 0],], [[0, 0],], [[0, 0],],
                        [[0, 0], [0, 1]], [[0, 0], [0, 1]], [[0, 0], [0, 1]],
                        [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], 
                        [[0, 0], [0, 1], [0, 2], [0, 3]]]
        
        self.msg = ""

    def find_ship_orientation(self, ship: list):
        """
        Finds given ship's orientation

        Args:
            ship (list): list containing ship's positions

        Returns:
            str: ship's orientation: 'Centered', 'Vertical' or 'Horizontal'
        """
        if len(ship) == 1:
            return "Centered"
        
        if ship[1][0] > ship[0][0]:
            return "Horizontal"
        if ship[1][1] > ship[0][1]:
            return "Vertical"

    def move_ship(self, ship: list, direction: str, ship_collection: list):
        """
        Moves given ship depending on the direction value

        Args:
            ship (list): list containing ship's positions
            direction (str): left, right, up or down
            ship_collection (list): list, where given ship is contained

        Returns:
            void method. Changes the positions of ship
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

    def rotate_ship(self, ship: list):
        """
        Rotates given ship based on it's orientation

        Args:
            ship (list): list containing ship's positions

        Returns:
            void method. Changes the positions of ship 
        """

        ship_orientation = self.find_ship_orientation(self.building_ships[-1])
        if ship_orientation != "Centered":
            if ship_orientation == "Vertical":
                for pos in ship[1:]:
                    index = ship.index(pos)

                    pos[0] += index
                    pos[1] -= index
            else:
                for pos in ship[1:]:
                    index = ship.index(pos)

                    pos[0] -= index
                    pos[1] += index

            if ship[-1][0] > 9:
                offset_x = ship[-1][0] - 9
                for pos in ship:
                    pos[0] -= offset_x

            if ship[-1][1] > 9:
                offset_y = ship[-1][1] - 9
                for pos in ship:
                    pos[1] -= offset_y

    def print_markers(self, stdscr, a_offset, n_offset=0):
        for i in range(len(self.alphabet)):
                stdscr.addstr(2, i * 3 + a_offset, self.alphabet[i])

        for i in range(1, 11):
            stdscr.addstr(i+2, 0 + n_offset, str(i))

    def print_player_grid(self, stdscr, colors, players_grid):
        for i in range(10):
            for j in range(10):
                if self.grid[i][j] == "[@]":
                    stdscr.addstr(i+3, j*3+3, players_grid[i][j], colors["CYAN"])
                else:
                    stdscr.addstr(i+3, j*3+3, players_grid[i][j])
    
    def print_enemy_grid(self, stdscr, colors, enemys_grid):
        for i in range(10):
            for j in range(10):
                if enemys_grid[i][j] == "[#]":
                    stdscr.addstr(i+3, j*3+53, enemys_grid[i][j], colors["YELLOW"])
                elif enemys_grid[i][j] == "[x]":
                    stdscr.addstr(i+3, j*3+53, enemys_grid[i][j], colors["RED"])
                else:
                    stdscr.addstr(i+3, j*3+53, enemys_grid[i][j])
