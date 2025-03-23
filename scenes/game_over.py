from sys import exit


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

        self.options = ["Restart", "Return to menu", "Exit"]
        self.current_option = 0

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

        for i in range(len(self.options)):
            if self.options[i] == self.options[self.current_option]:
                stdscr.addstr(i+4, 0, f"> {self.options[i]}")
            else:
                stdscr.addstr(i+4, 0, self.options[i])

        stdscr.refresh()

        key = stdscr.getkey()

        if key == "KEY_UP":
            self.current_option = max(0, self.current_option - 1)
        if key == "KEY_DOWN":
            self.current_option = min(len(self.options)-1, self.current_option + 1)
        if key in ["\n", "\r", "KEY_ENTER"]:
            if self.current_option == 0:
                if self.game_scene == "Player vs Computer":
                    self.player_vs_computer.reset()
                    self.game_state_manager.set_state(self.game_scene)
                elif self.game_scene == "Player vs Player":
                    self.player_vs_player.reset()
                    self.game_state_manager.set_state(self.game_scene)
            elif self.current_option == 1:
                self.game_state_manager.set_state("Main Menu")
            else:
                exit()
