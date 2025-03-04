class PlayerVsComputer:
    def __init__(self, game_state_manager):
        self.game_state_manager = game_state_manager

        self.alphabet = 'ABCDEFGHIJ'

        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.x, self.y = 0, 0
        self.x_step = 3
        self.y_step = 1
        self.building_ships = [([0, 0], [0, 1], [0, 2], [0, 3])]

        self.placing_ships = True
    
    def run(self, stdscr, colors):
        if self.placing_ships:
            stdscr.clear()

            for i in range(len(self.alphabet)):
                stdscr.addstr(0, i * 3 + 4, self.alphabet[i])

            for i in range(1, 11):
                stdscr.addstr(i, 0, str(i))

            for i in range(10):
                for j in range(len(self.grid[i])):
                    if self.grid[i][j] == "[@]":
                        stdscr.addstr(i+1, j*3+3, self.grid[i][j], colors["CYAN"])
                    else:
                        stdscr.addstr(i+1, j*3+3, self.grid[i][j])
                    
            for pos in self.building_ships[-1]:
                stdscr.addstr(pos[1]+1+self.y, pos[0]+3+self.x*3, "[@]", colors["CYAN"])

            stdscr.refresh()
            
            key = stdscr.getkey()
            if key == "KEY_LEFT":
                self.x = max(0, self.x - 1)
            if key == "KEY_RIGHT":
                self.x = min(9, self.x + 1)
            if key == "KEY_UP":
                self.y = max(0, self.y - 1)
            if key == "KEY_DOWN":
                self.y = min(10-len(self.building_ships[-1]), self.y + 1)
        else:
            pass
