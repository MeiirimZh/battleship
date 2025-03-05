class PlayerVsComputer:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.alphabet = 'ABCDEFGHIJ'

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [([0, 0],), ([0, 0],), ([0, 0],), ([0, 0],),
                        ([0, 0], [0, 1]), ([0, 0], [0, 1]), ([0, 0], [0, 1]),
                        ([0, 0], [0, 1], [0, 2]), ([0, 0], [0, 1], [0, 2]), 
                        ([0, 0], [0, 1], [0, 2], [0, 3])]

        self.offsets = [(0, 0), (1, 1), (1, 0),
                        (1, -1), (0, -1), (-1, -1),
                        (-1, 0), (-1, 1), (0, 1)]

        self.placing_ships = True

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

    def run(self, stdscr, colors):
        if self.placing_ships:
            msg = ""

            stdscr.clear()

            for i in range(len(self.alphabet)):
                stdscr.addstr(0, i * 3 + 4, self.alphabet[i])

            for i in range(1, 11):
                stdscr.addstr(i, 0, str(i))

            for i in range(10):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == "[@]":
                        stdscr.addstr(i+1, j*3+3, self.grid[i][j], colors["CYAN"])
                    else:
                        stdscr.addstr(i+1, j*3+3, self.grid[i][j])
    
            for pos in self.building_ships[-1]:
                if self.ship_contacts(self.building_ships[-1]):
                    stdscr.addstr(pos[1]+1, pos[0]*3+3, "[@]", colors["RED"])
                    msg = "You can't place a ship there!"
                else:
                    stdscr.addstr(pos[1]+1, pos[0]*3+3, "[@]", colors["GREEN"])

            # Ship position
            for i in range(len(self.building_ships[-1])):
                stdscr.addstr(i+14, 0, ", ".join([str(x) for x in self.building_ships[-1][i]]))

            if msg:
                stdscr.addstr(12, 0, msg)

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
            pass
