class PlayerVsComputer:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.alphabet = 'ABCDEFGHIJ'

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.placing_ships = True
    
    def run(self, stdscr):
        if self.placing_ships:
            stdscr.clear()

            for i in range(len(self.alphabet)):
                stdscr.addstr(0, i * 3 + 4, self.alphabet[i])

            for i in range(1, 11):
                stdscr.addstr(i, 0, str(i))

            for i in range(10):
                stdscr.addstr(i+1, 3, "".join(self.grid[i]))

            stdscr.refresh()
            stdscr.getch()
        else:
            pass
