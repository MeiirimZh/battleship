import copy
import random

from scenes.default_game_scene import DefaultGameScene


class PlayerVsPlayer(DefaultGameScene):
    def __init__(self, game_state_manager, game_over_scene):
        super().__init__(game_state_manager)
        self.game_over_scene = game_over_scene

        self.player_1_grid = copy.deepcopy(self.grid)
        self.player_2_grid = copy.deepcopy(self.grid)
        self.grids_dict = {"Player 1": self.player_1_grid, "Player 2": self.player_2_grid}

        self.player_1_x = 0
        self.player_1_y = 0
        self.player_2_x = 0
        self.player_2_y = 0

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
            if key in ["\n", "\r", "KEY_ENTER"]:
                self.place_ship(current_ship, self.ships_dict[self.turn], self.building_ships_dict[self.turn], self.grids_dict[self.turn])

                if not self.player_1_building_ships and self.turn == "Player 1":
                    self.player_1_init_ships = copy.deepcopy(self.player_1_ships)

                    self.print_player_grid(stdscr, colors, self.player_1_grid)

                    self.continue_action(stdscr)

                    self.turn = "Player 2"

                if not self.player_2_building_ships:
                    self.player_2_init_ships = copy.deepcopy(self.player_2_ships)

                    self.print_player_grid(stdscr, colors, self.player_2_grid)

                    self.continue_action(stdscr)
                    
                    self.placing_ships = False

        else:
            pass

    def continue_action(self, stdscr):
        stdscr.addstr(19, 0, "Press [Enter] to continue")
        stdscr.refresh()

        key = stdscr.getkey()

        while key not in ["\n", "\r", "KEY_ENTER"]:
            key = stdscr.getkey()
