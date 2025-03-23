import sys


class GameOver:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager
        self.player_vs_computer = None
        self.player_vs_player = None

        self.winner = ""
        self.player_1_name = ""
        self.player_2_name = ""
        self.player_1_score = 0
        self.player_2_score = 0
        self.game_scene = ""

        self.choices = ["Restart", "Return to menu", "Exit"]
        self.current_choice = 0

    def set_game_scenes(self, player_vs_computer, player_vs_player):
        self.player_vs_computer = player_vs_computer
        self.player_vs_player = player_vs_player

    def set_data(self, winner, player_1_name, player_2_name, player_1_score, player_2_score, game_scene):
        self.winner = winner
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        self.game_scene = game_scene
        
    def run(self, stdscr, colors):
        stdscr.clear()

        stdscr.addstr(0, 0, f"{self.winner} wins!", colors["YELLOW"])
        stdscr.addstr(1, 0, f"{self.player_1_name}: {self.player_1_score}")
        stdscr.addstr(2, 0, f"{self.player_2_name}: {self.player_2_score}")

        for i in range(len(self.choices)):
            if self.choices[i] == self.choices[self.current_choice]:
                stdscr.addstr(i+4, 0, f"> {self.choices[i]}")
            else:
                stdscr.addstr(i+4, 0, self.choices[i])

        stdscr.refresh()

        key = stdscr.getkey()

        if key == "KEY_UP":
            self.current_choice = max(0, self.current_choice - 1)
        if key == "KEY_DOWN":
            self.current_choice = min(len(self.choices)-1, self.current_choice + 1)
        if key in ["\n", "\r", "KEY_ENTER"]:
            if self.current_choice == 0:
                # self.player_vs_computer.reset()
                # self.game_state_manager.set_state("Player vs Computer")
                if self.game_scene == "Player vs Computer":
                    self.player_vs_computer.reset()
                    self.game_state_manager.set_state(self.game_scene)
                elif self.game_scene == "Player vs Player":
                    self.player_vs_player.reset()
                    self.game_state_manager.set_state(self.game_scene)
            elif self.current_choice == 1:
                pass
            else:
                sys.exit()
