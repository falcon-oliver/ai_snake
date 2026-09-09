from include.game.controls import LEFT, RIGHT, NO_MOVE
import torch
from torch import nn, argmax
from config.config import neural_network_config
from include.game.game_observer import GameObserver

INPUT_LAYER = 6
HIDDEN_LAYER = neural_network_config.hidden_layer
OUTPUT_LAYER = 3
MOVES = [NO_MOVE, LEFT, RIGHT]

class NeuralNetwork(nn.Module):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.game_observer = GameObserver(self.game)
        self.network = nn.Sequential(
            nn.Linear(INPUT_LAYER, HIDDEN_LAYER),
            nn.ReLU(),
            nn.Linear(HIDDEN_LAYER, OUTPUT_LAYER)
        )

    @torch.no_grad()
    def play_game(self):
        self.game._reset()
        self.game_observer = GameObserver(self.game)
        while not self.game.game_over:
            state = self.game_observer.state
            output = self(state)
            move = self._select_move(output)
            update = self.game.step(move)
            self.game_observer.update_state(update)
    
    def get_move(self, game_observer):
        output = self(game_observer.state)
        move = self._select_move(output)
        return move

    def load_network(self, state_dict):
        self.load_state_dict(state_dict)

    @property
    def fitness(self):
        return self.game_observer.fitness_score

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