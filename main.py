import time

from scenes.player_vs_computer import PlayerVsComputer
from scenes.player_vs_player import PlayerVsPlayer


class Game:
    def __init__(self):
        self.game_state_manager = GameStateManager("Player vs Computer")
        self.player_vs_computer = PlayerVsComputer(self.game_state_manager)
        self.player_vs_player = PlayerVsPlayer(self.game_state_manager)

        self.scenes = {"Player vs Computer": self.player_vs_computer, "Player vs Player": self.player_vs_player}

    def run(self):
        while True:
            self.scenes[self.game_state_manager.get_state()].run()

            time.sleep(.15)

``
class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state
    
    def set_state(self, state):
        self.current_state = state


if __name__ == "__main__":
    game = Game()
    game.run()
