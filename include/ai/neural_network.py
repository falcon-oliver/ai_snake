
import os
from include.game.controls import LEFT, RIGHT, NO_MOVE
import torch
from torch import nn, argmax
from torch.nn.utils import vector_to_parameters, parameters_to_vector
from include.game.game_state import GameState

INPUT_LAYER = 7
HIDDEN_LAYER = 12
OUTPUT_LAYER = 3
MOVES = [NO_MOVE, LEFT, RIGHT]
WEIGHT_FLOOR = -0.5
WEIGHT_CEIL = 0.5
torch.set_grad_enabled(False)
class NeuralNetwork(nn.Module):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.game_state = GameState(self.game)
        self.input_layer = nn.Linear(INPUT_LAYER, HIDDEN_LAYER)
        self.output_layer = nn.Linear(HIDDEN_LAYER, OUTPUT_LAYER)
        self.network = nn.Sequential(
            self.input_layer,
            nn.ReLU(),
            self.output_layer
        )

    def forward(self, state):
        return self.network(state)

    def load_weights(self, weights):
        vector_to_parameters(weights, self.network.parameters())

    def _select_move(self, output):
        move = argmax(output).item()
        return MOVES[move]

    def get_weights(self):
        return parameters_to_vector(self.network.parameters())

    def generate_random_weights(self):
        weights = self.get_weights()
        random_weights = torch.nn.init.uniform_(weights, WEIGHT_FLOOR, WEIGHT_CEIL)
        vector_to_parameters(random_weights, self.network.parameters())

    def play_game(self):
        while not self.game.game_over:
            state = self.game_state.game_state
            output = self(state)
            move = self._select_move(output)
            self.game.step(move)

    def get_move(self, game_state):
        state = game_state.game_state
        output = self(game_state.game_state)
        move = self._select_move(output)
        return move
        
    @property
    def fitness(self):
        return self.game_state.fitness_score