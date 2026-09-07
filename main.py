from argparse import ArgumentParser
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from warnings import filterwarnings
filterwarnings('ignore')
from include.ai.genetic_algorithm import GeneticAlgorithm
from include.game.game import Game
from include.game.renderer import Renderer

FPS = 60
class Main:
    def __init__(self):
        args = self._parse_args()
        self.train_game_width = 20
        self.train_game_height = 20
        self.game_width = 75
        self.game_height = 75
        self.window_width = 500
        self.window_height = 500
        self.start_population = 100
        self.iterations = 20
        self.ai = True
        self.game = Game(self.game_width, self.game_height)

    def _parse_args(self):
        parser = ArgumentParser(
            prog='Neuroevolution snake game',
            description='Utilising genetic algorithms and neural networks to play an AI-based solution to snake.'
        )

        parser.add_argument('-v', '--verbose', action='store_true')
        parser.add_argument('-f', '--file', action='store_true')
        return parser.parse_args()

    def _train(self):
        gen_algorithm = GeneticAlgorithm(self.train_game_width, self.train_game_height, self.start_population)
        gen_algorithm.train(self.iterations)
        neural_network = gen_algorithm.optimal_network
        return neural_network

    def _choose_ai(self, game_state, neural_network):
        current_move = neural_network.get_move(game_state)
        self.game.test_ai_step(current_move)

    def _choose(self):
        pass

    def _play_test(self):
        pass

    def _play_ai(self):
        neural_network = self._train()
        renderer = Renderer(self.game_width, self.game_height, self.window_width, self.window_height)
        frames = 0
        while True:
            if frames % 30 == 0:
                game_state = self.game.game_state
                current_move = neural_network.get_move(game_state)
                self.game.test_ai_step(current_move)
                renderer.render(game_state)
            if frames >= FPS:
                frames = 1
    
    def play(self):
        if self.ai:
            self._play_ai()
        else:
            self._play_test()

if __name__ == "__main__":
    main = Main()
    main.play()