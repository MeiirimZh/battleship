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

        self.placing_ships = False

    def run(self, stdscr, colors):
        if self.placing_ships:
            msg = ""

            stdscr.clear()

            stdscr.addstr(0, 9, "Place the ships")
            self.print_markers(stdscr, 4)
            self.print_player_grid(stdscr, colors, self.grid)
    
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

            if key in ["KEY_LEFT", "KEY_RIGHT", "KEY_UP", "KEY_DOWN"]:
                self.move_ship(self.building_ships[-1], key.split('_')[1].lower(), self.building_ships)
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
            self.print_player_grid(stdscr, colors, self.grid)
            self.print_enemy_grid(stdscr, colors, self.computer_display_grid)

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
                        self.destroy_ship(self.computer_display_grid, res)
                    else:
                        self.msg = "Hit!"
                else:
                    self.computer_display_grid[self.y][self.x] = "[o]"
            else:
                self.msg = ""
