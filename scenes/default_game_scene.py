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
        self.msg_2 = ""

        self.player_1_ships = ""
        self.player_2_ships = ""

        self.turn_msg = ""

        self.error_msg = ""

    def reset(self):
        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [[[0, 0],], [[0, 0],], [[0, 0],], [[0, 0],],
                        [[0, 0], [0, 1]], [[0, 0], [0, 1]], [[0, 0], [0, 1]],
                        [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], 
                        [[0, 0], [0, 1], [0, 2], [0, 3]]]
        
        self.msg = ""
        self.msg_2 = ""

        self.player_1_ships = ""
        self.player_2_ships = ""

        self.turn_msg = ""

        self.error_msg = ""

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

    def move_ship(self, ship: list, direction: str):
        """
        Moves given ship depending on the direction value

        Args:
            ship (list): list containing ship's positions
            direction (str): left, right, up or down

        Returns:
            void method. Changes the positions of ship
        """

        ship_orientation = self.find_ship_orientation(ship)

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

        ship_orientation = self.find_ship_orientation(ship)
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

    def place_ship(self, ship: list, ship_collection: list):
        if not self.ship_contacts(ship):
            for pos in ship:
                self.grid[pos[1]][pos[0]] = "[@]"
            ship_collection.append(ship)
            self.building_ships.remove(ship)

    def ship_contacts(self, ship: list):
        for pos in ship:
            for offset in self.offsets:
                x = pos[0] + offset[0]
                y = pos[1] + offset[1]
                if 0 <= x < 10 and 0 <= y < 10 and self.grid[y][x] == "[@]":
                    return True

    def destroy_ship(self, grid: list, ship: list):
        for pos in ship:
            grid[pos[1]][pos[0]] = "[x]"
        
        for pos in ship:
            for offset in self.offsets:
                offset_x = pos[0] + offset[0]
                offset_y = pos[1] + offset[1]
                if 0 <= offset_x <= 9 and 0 <= offset_y <= 9:
                    if grid[offset_y][offset_x] == "[ ]":
                        grid[offset_y][offset_x] = "[o]"

    def find_ship(self, x, y, ships_collection):
        for ship in ships_collection:
            for pos in ship:
                if pos[0] == x and pos[1] == y:
                    return ship
    
    def ship_destroyed(self, x, y, ships_collection, init_ships):
        for ship in ships_collection:
            for pos in ship:
                if pos[0] == x and pos[1] == y:
                    ship.remove(pos)
                    if len(ship) == 0:
                        ships_collection.remove([])

                        return self.find_ship(x, y, init_ships)

    def print_markers(self, stdscr, a_offset, n_offset=0):
        for i in range(len(self.alphabet)):
                stdscr.addstr(2, i * 3 + a_offset, self.alphabet[i])

        for i in range(1, 11):
            stdscr.addstr(i+2, 0 + n_offset, str(i))

    def print_player_grid(self, stdscr, colors, players_grid):
        for i in range(10):
            for j in range(10):
                if players_grid[i][j] == "[@]":
                    stdscr.addstr(i+3, j*3+3, players_grid[i][j], colors["CYAN"])
                elif players_grid[i][j] == "[#]":
                    stdscr.addstr(i+3, j*3+3, players_grid[i][j], colors["YELLOW"])
                elif players_grid[i][j] == "[x]":
                    stdscr.addstr(i+3, j*3+3, players_grid[i][j], colors["RED"])
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

    def all_ships_destroyed(self, ship_collection: list):
        return len(ship_collection) == 0

    def ships_left(self, ship_collection: list):
        return str(len(ship_collection))
