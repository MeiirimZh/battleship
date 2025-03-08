from scenes.default_game_scene import DefaultGameScene
from scripts.ai import AI


class PlayerVsComputer(DefaultGameScene):
    def __init__(self, game_state_manager):
        super().__init__(game_state_manager)

        self.computer = AI()
        self.computer.place_ships()

        self.computer_display_grid = [ ["[ ]" for j in range(10)] for i in range(10)]
        
        self.x = 0
        self.y = 0

        self.placing_ships = True

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
                elif self.computer_display_grid[i][j] == "[x]":
                    stdscr.addstr(i+3, j*3+53, self.computer_display_grid[i][j], colors["RED"])
                else:
                    stdscr.addstr(i+3, j*3+53, self.computer_display_grid[i][j])

    def destroy_ship(self, grid, x, y):
        ship = [[x, y]]

        grid[y][x] = "[x]"
        for offset in self.offsets:
            if x + offset[0] <= 9:
                offset_x = x + offset[0]
            if y + offset[1] <= 9:
                offset_y = y + offset[1]
            if grid[offset_y][offset_x] == "[#]":
                grid[offset_y][offset_x] = "[x]"
                ship.append([offset_x, offset_y])
                try:
                    while grid[offset_y + offset[1]][offset_x + offset[0]] == "[#]":
                        offset_x += offset[0]
                        offset_y += offset[1]
                        grid[offset_y][offset_x] = "[x]"
                        ship.append([offset_x, offset_y])
                except:
                    pass
        
        for pos in ship:
            for offset in self.offsets:
                offset_x = pos[0] + offset[0]
                offset_y = pos[1] + offset[1]
                if 0 <= offset_x <= 9 and 0 <= offset_y <= 9:
                    if grid[offset_y][offset_x] == "[ ]":
                        grid[offset_y][offset_x] = "[o]"

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
                self.move_ship(self.building_ships[-1], "left", self.building_ships)
            if key == "KEY_RIGHT":
                self.move_ship(self.building_ships[-1], "right", self.building_ships)
            if key == "KEY_UP":
                self.move_ship(self.building_ships[-1], "up", self.building_ships)
            if key == "KEY_DOWN":
                self.move_ship(self.building_ships[-1], "down", self.building_ships)
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

            stdscr.addstr(self.y+3, self.x*3+53, "[+]", colors["MAGENTA"])

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
                    if res:
                        self.msg = "Destroyed!"
                        self.destroy_ship(self.computer_display_grid, self.x, self.y)
                    else:
                        self.msg = "Hit!"
                else:
                    self.computer_display_grid[self.y][self.x] = "[o]"
            else:
                self.msg = ""
