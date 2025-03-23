class Settings:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.options = ["Markers", "Colors", "Exit"]
        self.current_option = 0

        self.current_state = "Choice"

    def run(self, stdscr, colors):
        stdscr.clear()

        if self.current_state == "Choice":
            stdscr.addstr(0, 0, "Settings", colors["CYAN"])

            for i in range(len(self.options)):
                if self.options[i] == self.options[self.current_option]:
                    stdscr.addstr(i+2, 0, f"> {self.options[i]}")
                else:
                    stdscr.addstr(i+2, 0, self.options[i])

            stdscr.refresh()

            key = stdscr.getkey()

            if key == "KEY_UP":
                self.current_option = max(0, self.current_option - 1)
            if key == "KEY_DOWN":
                self.current_option = min(len(self.options)-1, self.current_option + 1)
            if key in ["\n", "\r", "KEY_ENTER"]:
                if self.current_option == 0:
                    pass
                elif self.current_option == 1:
                    pass
                else:
                    self.game_state_manager.set_state("Main Menu")
