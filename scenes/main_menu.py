from sys import exit


class MainMenu:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.options = ["Player vs Computer", "Player vs Player", "Settings", "Exit"]
        self.current_option = 0

    def run(self, stdscr, colors):
        stdscr.clear()

        stdscr.addstr(0, 0, "Battleship", colors["CYAN"])

        for i in range(len(self.options)):
            if self.options[i] == self.options[self.current_option]:
                stdscr.addstr(i+2, 0, f"> {self.options[i]}")
            else:
                stdscr.addstr(i+2, 0, self.options[i])

        stdscr.addstr(7, 0, "Made by Zhanzhumanov Meiirim 2025")

        stdscr.refresh()
            
        key = stdscr.getkey()

        if key == "KEY_UP":
            self.current_option = max(0, self.current_option - 1)
        if key == "KEY_DOWN":
            self.current_option = min(len(self.options)-1, self.current_option + 1)
        if key in ["\n", "\r", "KEY_ENTER"]:
            if self.current_option == 0:
                self.game_state_manager.set_state("Player vs Computer")
            elif self.current_option == 1:
                self.game_state_manager.set_state("Player vs Player")
            else:
                exit()
