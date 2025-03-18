class GameOver:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.winner = ""
        self.player_1_name = ""
        self.player_2_name = ""
        self.player_1_score = 0
        self.player_2_score = 0

    def get_data(self, winner, player_1_name, player_2_name, player_1_score, player_2_score):
        self.winner = winner
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name
        self.player_1_score = player_1_score
        self.player_2_score = player_2_score
        
    def run(self, stdscr, colors):
        stdscr.clear()

        stdscr.addstr(0, 0, f"{self.winner} wins!", colors["YELLOW"])
        stdscr.addstr(1, 0, f"{self.player_1_name}: {self.player_1_score}")
        stdscr.addstr(2, 0, f"{self.player_2_name}: {self.player_2_score}")

        stdscr.refresh()

        key = stdscr.getkey()
