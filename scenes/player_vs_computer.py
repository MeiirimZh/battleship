from scripts.ai import AI


class PlayerVsComputer:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.computer = AI()
        self.computer.place_ships()

        self.alphabet = 'ABCDEFGHIJ'

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]
        self.computer_display_grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [([0, 0],), ([0, 0],), ([0, 0],), ([0, 0],),
                        ([0, 0], [0, 1]), ([0, 0], [0, 1]), ([0, 0], [0, 1]),
                        ([0, 0], [0, 1], [0, 2]), ([0, 0], [0, 1], [0, 2]), 
                        ([0, 0], [0, 1], [0, 2], [0, 3])]

        self.offsets = [(0, 0), (1, 1), (1, 0),
                        (1, -1), (0, -1), (-1, -1),
                        (-1, 0), (-1, 1), (0, 1)]
        
        self.x = 0
        self.y = 0

        self.placing_ships = False
        self.msg = ""

    def move_ship(self, ship: tuple, direction: str):
        ship_orientation = self.find_ship_orientation(self.building_ships[-1])
        
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

    def rotate_ship(self, ship):
        ship_orientation = self.find_ship_orientation(self.building_ships[-1])
        if ship_orientation != "Centered":
            if ship_orientation == "Vertical":
                i = ship[0][0]
                for pos in ship[1:]:
                    i += 1
                    pos[0], pos[1] = i, ship[0][1]

                if ship[-1][0] > 9:
                    offset = ship[-1][0] - 9

                    for pos in ship:
                        pos[0] -= offset
            else:
                i = ship[0][1]
                for pos in ship[1:]:
                    i += 1
                    pos[0], pos[1] = ship[0][0], i
                
                if ship[-1][1] > 9:
                    offset = ship[-1][1] - 9

                    for pos in ship:
                        pos[1] -= offset

    def find_ship_orientation(self, ship):
        if len(ship) == 1:
            return "Centered"
        
        if ship[1][0] > ship[0][0]:
            return "Horizontal"
        if ship[1][1] > ship[0][1]:
            return "Vertical"
    
    def ship_contacts(self, ship):
        for pos in ship:
            for offset in self.offsets:
                x = pos[0] + offset[0]
                y = pos[1] + offset[1]
                if 0 <= x < 10 and 0 <= y < 10 and self.grid[y][x] == "[@]":
                    return True

    def place_ship(self, ship):
        if not self.ship_contacts(ship):
            for pos in ship:
                self.grid[pos[1]][pos[0]] = "[@]"
            self.building_ships.remove(ship)

    def print_markers(self, stdscr, a_offset, n_offset=0):
        for i in range(len(self.alphabet)):
                stdscr.addstr(2, i * 3 + a_offset, self.alphabet[i])

        for i in range(1, 11):
            stdscr.addstr(i+2, 0 + n_offset, str(i))

    def print_player_grid(self, stdscr, colors):
        for i in range(10):
            for j in range(10):
                if self.grid[i][j] == "[@]":
                    stdscr.addstr(i+3, j*3+3, self.grid[i][j], colors["CYAN"])
                else:
                    stdscr.addstr(i+3, j*3+3, self.grid[i][j])

    def print_enemy_grid(self, stdscr, colors):
        for i in range(10):
            for j in range(10):
                if self.computer_display_grid[i][j] == "[#]":
                    stdscr.addstr(i+3, j*3+53, self.computer_display_grid[i][j], colors["YELLOW"])
                else:
                    stdscr.addstr(i+3, j*3+53, self.computer_display_grid[i][j])

    def run(self, stdscr, colors):
        if self.placing_ships:
            msg = ""

            stdscr.clear()

            stdscr.addstr(0, 9, "Place the ships")
            self.print_markers(stdscr, 4)
            self.print_player_grid(stdscr, colors)
    
            for pos in self.building_ships[-1]:
                if self.ship_contacts(self.building_ships[-1]):
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["RED"])
                    msg = "You can't place a ship there!"
                else:
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["GREEN"])

            # Ship position
            for i in range(len(self.building_ships[-1])):
                stdscr.addstr(i+16, 0, ", ".join([str(x + 1) for x in self.building_ships[-1][i]]))

            if msg:
                stdscr.addstr(14, 0, msg)

            stdscr.refresh()
            
            key = stdscr.getkey()

            if key == "KEY_LEFT":
                self.move_ship(self.building_ships[-1], "left")
            if key == "KEY_RIGHT":
                self.move_ship(self.building_ships[-1], "right")
            if key == "KEY_UP":
                self.move_ship(self.building_ships[-1], "up")
            if key == "KEY_DOWN":
                self.move_ship(self.building_ships[-1], "down")
            if key.lower() == "r":
                self.rotate_ship(self.building_ships[-1])
            if key in ["\n", "\r", "KEY_ENTER"]:
                self.place_ship(self.building_ships[-1])
                if not self.building_ships:
                    self.placing_ships = False
        
        else:
            stdscr.clear()

            stdscr.addstr(0, 12, "Your grid")
            stdscr.addstr(0, 62, "Enemy grid")
            self.print_markers(stdscr, 4)
            self.print_player_grid(stdscr, colors)
            self.print_enemy_grid(stdscr, colors)

            stdscr.addstr(self.y+3, self.x*3+53, "[x]", colors["RED"])

            self.print_markers(stdscr, 54, 50)

            if self.msg:
                stdscr.addstr(14, 0, self.msg)

            stdscr.refresh()
            
            key = stdscr.getkey()

            if key == "KEY_LEFT":
                self.x = max(0, self.x - 1)
            if key == "KEY_RIGHT":
                self.x = min(9, self.x + 1)
            if key == "KEY_UP":
                self.y = max(0, self.y - 1)
            if key == "KEY_DOWN":
                self.y = min(9, self.y + 1)
            if key in ["\n", "\r", "KEY_ENTER"]:
                if self.computer.grid[self.y][self.x] == "[@]":
                    self.computer_display_grid[self.y][self.x] = "[#]"
                    self.computer.grid[self.y][self.x] = "[ ]"
                    res = self.computer.ship_destroyed(self.x, self.y)
                    self.msg = "Destroyed!" if res else "Hit!"
                else:
                    self.computer_display_grid[self.y][self.x] = "[o]"
            else:
                self.msg = ""
