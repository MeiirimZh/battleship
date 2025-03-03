import curses
import time
from curses import wrapper

from scenes.player_vs_computer import PlayerVsComputer
from scenes.player_vs_player import PlayerVsPlayer


class Game:
    def __init__(self):
        self.game_state_manager = GameStateManager("Player vs Computer")
        self.player_vs_computer = PlayerVsComputer(self.game_state_manager)
        self.player_vs_player = PlayerVsPlayer(self.game_state_manager)

        self.scenes = {"Player vs Computer": self.player_vs_computer, "Player vs Player": self.player_vs_player}

    def run(self, stdscr):
        while True:
            self.scenes[self.game_state_manager.get_state()].run(stdscr)

            time.sleep(.15)


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state
    
    def set_state(self, state):
        self.current_state = state


def main(stdscr):
    game = Game()
    game.run(stdscr)


if __name__ == "__main__":
    wrapper(main)
