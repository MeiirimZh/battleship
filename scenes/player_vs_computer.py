import copy
import random
import time

from scenes.default_game_scene import DefaultGameScene
from scripts.ai import AI


class PlayerVsComputer(DefaultGameScene):
    def __init__(self, game_state_manager, game_over_scene):
        super().__init__(game_state_manager)
        self.game_over_scene = game_over_scene

        self.computer = AI(self)
        self.computer.place_ships()

        self.computer_display_grid = [ ["[ ]" for j in range(10)] for i in range(10)]
        
        self.x = 0
        self.y = 0

        self.placing_ships = True

        self.ships = []
        self.init_ships = []

        self.player_turn = random.choice([True, False])

        self.player_wins = 0
        self.computer_wins = 0

    def reset(self):
        super().reset()

        self.x = 0
        self.y = 0

        self.placing_ships = True

        self.ships = []
        self.init_ships = []

        self.player_turn = random.choice([True, False])

        self.computer.reset()

        self.computer.place_ships()

        self.computer_display_grid = [ ["[ ]" for j in range(10)] for i in range(10)]

    def run(self, stdscr, colors):
        if self.placing_ships:
            msg = "Ship position:"

            stdscr.clear()

            stdscr.addstr(0, 9, "Place the ships")
            self.print_markers(stdscr, 4)
            self.print_player_grid(stdscr, colors, self.grid)

            for pos in self.building_ships[-1]:
                if self.ship_contacts(self.building_ships[-1], self.grid):
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["RED"])
                    msg = "You can't place a ship there!"
                else:
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["GREEN"])

            for i in range(len(self.building_ships[-1])):
                stdscr.addstr(i+16, 0, ", ".join([str(x + 1) for x in self.building_ships[-1][i]]))

            if msg:
                stdscr.addstr(14, 0, msg)

            stdscr.refresh()
            
            key = stdscr.getkey()

            if key in ["KEY_LEFT", "KEY_RIGHT", "KEY_UP", "KEY_DOWN"]:
                self.move_ship(self.building_ships[-1], key.split('_')[1].lower())
            if key.lower() == "r":
                self.rotate_ship(self.building_ships[-1])
            if key in ["\n", "\r", "KEY_ENTER"]:
                self.place_ship(self.building_ships[-1], self.ships, self.building_ships, self.grid)
                if not self.building_ships:
                    self.init_ships = copy.deepcopy(self.ships)
                    
                    self.placing_ships = False
        
        else:
            stdscr.clear()

            stdscr.addstr(0, 12, "Your grid")
            stdscr.addstr(0, 62, "Enemy grid")
            self.print_markers(stdscr, 4)
            self.print_player_grid(stdscr, colors, self.grid)
            self.print_enemy_grid(stdscr, colors, self.computer_display_grid)

            self.player_1_ships = f'Player ships: {self.ships_left(self.ships)}'
            self.player_2_ships = f'Enemy ships: {self.ships_left(self.computer.ships)}'

            if self.player_turn:
                self.turn_msg = "Your turn"

                stdscr.addstr(self.y+3, self.x*3+53, "[+]", colors["CYAN"])
            else:
                self.turn_msg = "Computer's turn"

            stdscr.addstr(14, 0, self.turn_msg)

            if self.msg:
                stdscr.addstr(15, 0, self.msg)

            if self.msg_2:
                stdscr.addstr(16, 0, self.msg_2)

            if self.player_1_ships:
                stdscr.addstr(17, 0, self.player_1_ships)

            if self.player_2_ships:
                stdscr.addstr(18, 0, self.player_2_ships)

            if self.error_msg:
                stdscr.addstr(20, 0, self.error_msg)

            self.print_markers(stdscr, 54, 50)

            stdscr.refresh()

            if self.player_turn:
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
                        self.computer.grid[self.y][self.x] = "[#]"

                        res = self.ship_destroyed(self.x, self.y, self.computer.ships, self.computer.init_ships)
                        if res:
                            self.msg = "Player: Destroyed!"
                            self.destroy_ship(self.computer_display_grid, res)
                            
                            if self.all_ships_destroyed(self.computer.ships):
                                self.player_wins += 1
                                self.game_over_scene.set_data("Player", "Player", "Computer", self.player_wins, self.computer_wins)
                                self.game_state_manager.set_state("Game Over")
                        else:
                            self.msg = "Player: Hit!"

                    elif self.computer.grid[self.y][self.x] == "[ ]" and self.computer_display_grid[self.y][self.x] != "[o]":
                        self.computer_display_grid[self.y][self.x] = "[o]"

                        self.player_turn = False
                else:
                    self.msg = ""
            else:
                time.sleep(2)
                
                attack = self.computer.attack(self.grid)
                if attack == "Miss!":
                    self.msg_2 = ""
                    self.player_turn = True
                elif attack == None:
                    self.msg = ""
                else:
                    self.msg_2 = f'Computer: {attack}'
                    if self.all_ships_destroyed(self.ships):
                        self.computer_wins += 1
                        self.game_over_scene.set_data("Computer", "Player", "Computer", self.player_wins, self.computer_wins)
                        self.game_state_manager.set_state("Game Over")
