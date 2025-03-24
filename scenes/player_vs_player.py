import copy
import random

from scenes.default_game_scene import DefaultGameScene


class PlayerVsPlayer(DefaultGameScene):
    def __init__(self, game_state_manager, data, game_over_scene):
        super().__init__(game_state_manager, data)
        self.game_over_scene = game_over_scene

        self.player_1_grid = copy.deepcopy(self.grid)
        self.player_2_grid = copy.deepcopy(self.grid)
        self.grids_dict = {"Player 1": self.player_1_grid, "Player 2": self.player_2_grid}

        self.x = 0
        self.y = 0

        self.player_1_ships = []
        self.player_1_init_ships = []
        self.player_2_ships = []
        self.player_2_init_ships = []
        self.ships_dict = {"Player 1": self.player_1_ships, "Player 2": self.player_2_ships}

        self.placing_ships = True

        self.player_1_building_ships = copy.deepcopy(self.building_ships)
        self.player_2_building_ships = copy.deepcopy(self.building_ships)
        self.building_ships_dict = {"Player 1": self.player_1_building_ships, "Player 2": self.player_2_building_ships}

        self.turn = "Player 1"

        self.player_1_wins = 0
        self.player_2_wins = 0

    def reset(self):
        super().reset()

        self.x = 0
        self.y = 0

        self.player_1_grid = copy.deepcopy(self.grid)
        self.player_2_grid = copy.deepcopy(self.grid)
        self.grids_dict = {"Player 1": self.player_1_grid, "Player 2": self.player_2_grid}

        self.player_1_ships = []
        self.player_1_init_ships = []
        self.player_2_ships = []
        self.player_2_init_ships = []
        self.ships_dict = {"Player 1": self.player_1_ships, "Player 2": self.player_2_ships}

        self.placing_ships = True

        self.player_1_building_ships = copy.deepcopy(self.building_ships)
        self.player_2_building_ships = copy.deepcopy(self.building_ships)
        self.building_ships_dict = {"Player 1": self.player_1_building_ships, "Player 2": self.player_2_building_ships}

        self.turn = "Player 1"
    
    def run(self, stdscr, colors):
        if self.placing_ships:
            msg = "Ship position:"
            
            current_ship = self.building_ships_dict[self.turn][-1]

            stdscr.clear()

            stdscr.addstr(0, 6, f"Place the ships: {self.turn}")

            self.print_markers(stdscr, 4)
            if self.turn == "Player 1":
                self.print_player_grid(stdscr, colors, self.player_1_grid)
            else:
                self.print_player_grid(stdscr, colors, self.player_2_grid)

            for pos in current_ship:
                if self.ship_contacts(current_ship, self.grids_dict[self.turn]):
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["RED"])
                    msg = "You can't place a ship there!"
                else:
                    stdscr.addstr(pos[1]+3, pos[0]*3+3, "[@]", colors["GREEN"])

            for i in range(len(self.building_ships_dict[self.turn][-1])):
                stdscr.addstr(i+16, 0, ", ".join([str(x + 1) for x in current_ship[i]]))

            if msg:
                stdscr.addstr(14, 0, msg)

            stdscr.refresh()
            
            key = stdscr.getkey()

            if key in ["KEY_LEFT", "KEY_RIGHT", "KEY_UP", "KEY_DOWN"]:
                self.move_ship(current_ship, key.split('_')[1].lower())
            if key.lower() == "r":
                self.rotate_ship(current_ship)
            if key == "\x1b":
                self.game_state_manager.set_state("Main Menu")
            if key in ["\n", "\r", "KEY_ENTER"]:
                self.place_ship(current_ship, self.ships_dict[self.turn], self.building_ships_dict[self.turn], self.grids_dict[self.turn])

                if not self.player_1_building_ships and self.turn == "Player 1":
                    self.player_1_init_ships = copy.deepcopy(self.player_1_ships)

                    self.print_player_grid(stdscr, colors, self.player_1_grid)

                    self.continue_action(stdscr, 19)

                    self.turn = "Player 2"

                if not self.player_2_building_ships:
                    self.player_2_init_ships = copy.deepcopy(self.player_2_ships)
                    self.init_ships_dict = {"Player 1": self.player_1_init_ships, "Player 2": self.player_2_init_ships}

                    self.print_player_grid(stdscr, colors, self.player_2_grid)

                    self.continue_action(stdscr, 19)

                    self.turn = random.choice(["Player 1", "Player 2"])

                    stdscr.clear()

                    stdscr.addstr(0, 0, f'{self.turn} starts first')
                    self.continue_action(stdscr, 2)
                    
                    self.placing_ships = False

        else:
            stdscr.clear()

            stdscr.addstr(0, 12, "Your grid")
            stdscr.addstr(0, 62, "Enemy grid")
            self.print_markers(stdscr, 4)
            self.print_markers(stdscr, 54, 50)
            self.print_player_grid(stdscr, colors, self.grids_dict[self.turn])
            if self.turn == "Player 1":
                self.print_enemy_grid(stdscr, colors, self.player_2_grid)
            else:
                self.print_enemy_grid(stdscr, colors, self.player_1_grid)

            self.player_1_ships_msg = f'Player 1 ships: {self.ships_left(self.player_1_ships)}'
            self.player_2_ships_msg = f'Player 2 ships: {self.ships_left(self.player_2_ships)}'

            if self.turn == "Player 1":
                self.turn_msg = "Player 1's turn"
            else:
                self.turn_msg = "Player 2's turn"

            stdscr.addstr(self.y+3, self.x*3+53, "[+]", colors["CYAN"])

            stdscr.addstr(14, 0, self.turn_msg)

            if self.msg:
                stdscr.addstr(15, 0, self.msg)

            if self.player_1_ships_msg:
                stdscr.addstr(17, 0, self.player_1_ships_msg)

            if self.player_2_ships_msg:
                stdscr.addstr(18, 0, self.player_2_ships_msg)

            stdscr.refresh()

            key = stdscr.getkey()

            opponent = "Player 2" if self.turn == "Player 1" else "Player 1"

            if key == "KEY_LEFT":
                self.x = max(0, self.x - 1)
            if key == "KEY_RIGHT":
                self.x = min(9, self.x + 1)
            if key == "KEY_UP":
                self.y = max(0, self.y - 1)
            if key == "KEY_DOWN":
                self.y = min(9, self.y + 1)
            if key == "\x1b":
                self.game_state_manager.set_state("Main Menu")
            if key in ["\n", "\r", "KEY_ENTER"]:
                if self.grids_dict[opponent][self.y][self.x] == "[@]":
                    self.grids_dict[opponent][self.y][self.x] = "[#]"

                    res = self.ship_destroyed(self.x, self.y, self.ships_dict[opponent], self.init_ships_dict[opponent])

                    if res:
                        self.msg = "Destroyed!"
                        self.destroy_ship(self.grids_dict[opponent], res)

                        if self.all_ships_destroyed(self.ships_dict[opponent]):
                            if self.turn == "Player 1":
                                self.player_1_wins += 1
                                self.game_over_scene.set_data("Player 1", "Player 1", "Player 2", self.player_1_wins, self.player_2_wins, "Player vs Player")
                            else:
                                self.player_2_wins += 1
                                self.game_over_scene.set_data("Player 2", "Player 1", "Player 2", self.player_1_wins, self.player_2_wins, "Player vs Player")
                            self.game_state_manager.set_state("Game Over")
                    else:
                        self.msg = "Hit!"
                elif self.grids_dict[opponent][self.y][self.x] == "[ ]" and self.grids_dict[opponent][self.y][self.x] != "[o]":
                    self.grids_dict[opponent][self.y][self.x] = "[o]"

                    self.continue_action(stdscr, 19)

                    self.turn = opponent
            else:
                self.msg = ""

    def continue_action(self, stdscr, y):
        stdscr.addstr(y, 0, "Press [Enter] to continue")
        stdscr.refresh()

        key = stdscr.getkey()

        while key not in ["\n", "\r", "KEY_ENTER"]:
            key = stdscr.getkey()
