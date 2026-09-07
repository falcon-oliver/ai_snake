
import os
from include.game.controls import LEFT, RIGHT, NO_MOVE
import torch
from torch import nn, argmax

INPUT_LAYER = 6
HIDDEN_LAYER = 10
OUTPUT_LAYER = 3
MOVES = [NO_MOVE, LEFT, RIGHT]
WEIGHT_FLOOR = -0.5
WEIGHT_CEIL = 0.5
class NeuralNetwork(nn.Module):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.game_state = self.game.game_state
        self.input_layer = nn.Linear(INPUT_LAYER, HIDDEN_LAYER)
        self.output_layer = nn.Linear(HIDDEN_LAYER, OUTPUT_LAYER)
        self.network = nn.Sequential(
            nn.Linear(INPUT_LAYER, HIDDEN_LAYER),
            nn.ReLU(),
            nn.Linear(HIDDEN_LAYER, OUTPUT_LAYER)
        )

    @torch.no_grad()
    def play_game(self):
        self.game._reset()
        self.game_state = self.game.game_state
        self.game.game_state.snacks_ate = 0
        self.game.game_state.time_survived = 0

        while not self.game.game_over:
            state = self.game.game_state.game_state
            output = self(state)
            move = self._select_move(output)
            self.game.step_ai(move)
    
    def get_move(self, game_state):
        output = self(game_state.game_state)
        move = self._select_move(output)
        return move
        
    @property
    def fitness(self):
        self.game_state = self.game.game_state
        return self.game_state.fitness_score

    @torch.no_grad()
    def _load_param(self, values, param_name):
        current_index = 0
        for name, param in self.named_parameters():
            if param_name in name:
                elements = param.numel()
                segment = values[current_index : current_index + elements]
                layer_shape = param.shape
                weight = segment.view(layer_shape)
                param.copy_(weight)
                current_index += elements

    def _select_move(self, output):
        move = argmax(output).item()
        return MOVES[move]

    def _get_param(self, param_name):
        values = []
        for name, param in self.named_parameters():
            if param_name in name:
                values.append(param.detach().flatten())
        return torch.cat(values)

    def forward(self, state):
        return self.network(state)
    
    def load_weights(self, weights):
        self._load_param(weights, 'weight')    

    def load_bias(self, bias):
        self._load_param(bias, 'bias')
    
    def get_weights(self):
        return self._get_param('weight')

    def get_bias(self):
        return self._get_param('bias')