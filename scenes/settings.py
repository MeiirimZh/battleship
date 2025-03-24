import curses


class Settings:
    def __init__(self, game_state_manager, data):
        self.game_state_manager = game_state_manager
        self.data = data

        self.options = ["Markers", "Colors", "Exit"]
        self.current_option = 0

        self.markers = [self.data.ship_marker, self.data.hit_marker, self.data.destroyed_marker, self.data.miss_marker]
        self.marker_names = ["Ship marker", "Hit marker", "Destroyed marker", "Miss marker"]
        self.current_marker = 0

        self.current_state = "Choice"

    def run(self, stdscr, colors):
        curses.echo()

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
                    self.current_state = "Markers"
                elif self.current_option == 1:
                    pass
                else:
                    self.game_state_manager.set_state("Main Menu")
        elif self.current_state == "Markers":
            stdscr.addstr(0, 0, "Markers", colors["CYAN"])

            stdscr.addstr(2, 0, f'{self.marker_names[self.current_marker]}, currently used:')
            stdscr.addstr(2, len(f'{self.marker_names[self.current_marker]}, currently used:') + 1,
                          self.markers[self.current_marker], colors["YELLOW"])
            stdscr.addstr(4, 0, "Enter a new marker ([Enter] to skip):")

            for i in range(len(self.markers)):
                stdscr.addstr(i+8, 0, f'{self.marker_names[i]}: {self.markers[i]}')

            marker_changed = False

            while not marker_changed:
                stdscr.addstr(4, 38, " ")

                new_marker = stdscr.getstr(4, 38, 1).decode("utf-8")

                if new_marker == "":
                    if self.current_marker == len(self.markers) - 1:
                        stdscr.clear()

                        for i in range(len(self.markers)):
                            stdscr.addstr(i, 0, f'{self.marker_names[i]}: {self.markers[i]}')

                        stdscr.addstr(len(self.markers)+1, 0, "Settings saved. Press [Enter] to return to Settings.")

                        stdscr.refresh()

                        key = stdscr.getkey()

                        while key not in ["\n", "\r", "KEY_ENTER"]:
                            key = stdscr.getkey()

                        self.current_marker = 0
                        self.current_state = "Choice"
                    else:
                        self.current_marker += 1

                    marker_changed = True
                else:
                    if f'[{new_marker}]' in self.markers:
                        stdscr.addstr(6, 0, f"Marker [{new_marker}] already exists! Try again.", colors["RED"])
                        stdscr.refresh()
                        continue
                    else:
                        if self.current_marker == 0:
                            self.data.ship_marker = f'[{new_marker}]'
                        elif self.current_marker == 1:
                            self.data.hit_marker = f'[{new_marker}]'
                        elif self.current_marker == 2:
                            self.data.destroyed_marker = f'[{new_marker}]'
                        else:
                            self.data.miss_marker = f'[{new_marker}]'

                        self.markers = [self.data.ship_marker, self.data.hit_marker, self.data.destroyed_marker, self.data.miss_marker]

                        if self.current_marker == len(self.markers) - 1:
                            stdscr.clear()

                            for i in range(len(self.markers)):
                                stdscr.addstr(i, 0, f'{self.marker_names[i]}: {self.markers[i]}')

                            stdscr.addstr(len(self.markers)+1, 0, "Settings saved. Press [Enter] to return to Settings.")

                            stdscr.refresh()

                            key = stdscr.getkey()

                            while key not in ["\n", "\r", "KEY_ENTER"]:
                                key = stdscr.getkey()

                            self.current_marker = 0
                            self.current_state = "Choice"
                        else:
                            self.current_marker += 1

                        marker_changed = True

            stdscr.refresh()
