from argparse import ArgumentParser
from os import environ
from pathlib import Path
from include.ai.neural_network import NeuralNetwork
from include.game.game_observer import GameObserver
from include.game.handle_input import InputHandler
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from warnings import filterwarnings
filterwarnings('ignore')
from include.ai.genetic_algorithm import GeneticAlgorithm
from include.game.game import Game
from include.game.renderer import Renderer
import torch
from random import random

class Main:
    def __init__(self):
        args = self._parse_args()
        self.train_game_width = 20
        self.train_game_height = 20
        self.game_width = 50
        self.game_height = 50
        self.window_width = 500
        self.window_height = 500
        self.ai = not args.test_play if args.test_play is not None else False
        self.save_model = args.save_model is not None
        self.save_name = args.save_model if args.save_model else f'./models/{int(random()*10000)}.pt'
        self.load_model = args.load_model is not None
        self.load_name = args.load_model if args.load_model else './models/example.pt'
        self.start_population = args.population if args.population is not None else 100
        self.iterations = args.iterations if args.iterations is not None else 20
        self.game = Game(self.game_width, self.game_height)

    def _parse_args(self):
        parser = ArgumentParser(
            prog='Neuroevolution snake game',
            description='Utilising genetic algorithms and neural networks to play an AI-based solution to snake.'
        )
        parser.add_argument('-p', '--population', type=int)
        parser.add_argument('-i', '--iterations', type=int)
        parser.add_argument('-s', '--save-model', type=Path, default=None)
        parser.add_argument('-l', '--load-model', type=Path, default=None)
        parser.add_argument('-t', '--test-play', action='store_true')
        return parser.parse_args()

    def _train(self):
        gen_algorithm = GeneticAlgorithm(self.train_game_width, self.train_game_height, self.start_population)
        gen_algorithm.train(self.iterations)
        neural_network = gen_algorithm.optimal_network
        return neural_network

    def _load_model(self):
        state_dict = torch.load(self.load_name)
        neural_network = NeuralNetwork(self.game)
        neural_network.load_network(state_dict)
        return neural_network

    def _play_ai(self):
        neural_network  = None
        if self.load_model:
            neural_network = self._load_model()
        else:
            neural_network = self._train()
            if self.save_model:
                torch.save(neural_network.state_dict(), self.save_name)
        renderer = Renderer(self.game_width, self.game_height, self.window_width, self.window_height)
        observer = GameObserver(self.game)
        while True:
            current_move = neural_network.get_move(observer)
            self.game.step(current_move, timeout_enabled=False)
            renderer.render(observer)
            if self.game.game_over:
                self.game._reset()

    def _play_test(self):
        input_handler = InputHandler()
        renderer = Renderer(self.game_width, self.game_height, self.window_width, self.window_height)
        observer = GameObserver(self.game)
        while True:
            if self.game.game_over:
                self.game._reset()
            current_move = input_handler.get_move()
            update = self.game.step(current_move, timeout_enabled=False, relative=False)
            state = observer.state
            observer.update_state(update)
            renderer.render(observer)
            if self.game.game_over:
                self.game._reset()
    
    def play(self):
        if self.ai:
            self._play_ai()
        else:
            self._play_test()

if __name__ == "__main__":
    main = Main()
    main.play()