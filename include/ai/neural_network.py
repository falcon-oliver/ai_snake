
import os
from include.game.controls import LEFT, RIGHT, NO_MOVE
import torch
from torch import nn, argmax

INPUT_LAYER = 7
HIDDEN_LAYER = 50
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
            self.input_layer,
            nn.ReLU(),
            self.output_layer
        )

    def forward(self, state):
        output = self.network(state)
        return output

    def load_weights(self, weights):
        current = 0
        with torch.no_grad():
            for name, param in self.named_parameters():
                if "weight" in name:
                    elements = param.numel()
                    segment = weights[current : current + elements]
                    layer_shape = param.shape
                    weight = segment.view(layer_shape)
                    param.copy_(weight)
                    current += elements

    def _select_move(self, output):
        move = argmax(output).item()
        return MOVES[move]

    def get_weights(self):
        weights = []
        for name, param in self.named_parameters():
            if "weight" in name:
                weights.append(param.detach().flatten())
        return torch.cat(weights)
    
    def play_game(self):
        self.game._reset()
        self.game_state = self.game.game_state
        self.game.game_state.snacks_ate = 0
        self.game.game_state.time_survived = 0

        inactive_max = 55
        inactive_count = 0
        snacks_ate = 0
        
        while not self.game.game_over:
            state = self.game.game_state.game_state
            output = self(state)
            move = self._select_move(output)

            self.game.step_ai(move)

            if self.game.game_state.snacks_ate == snacks_ate:
                inactive_count += 1
            else:
                snacks_ate = self.game.game_state.snacks_ate
                inactive_count = 0

            if inactive_count >= inactive_max:
                self.game.game_over = True

    def get_move(self, game_state):
        output = self(game_state.game_state)
        move = self._select_move(output)
        return move
        
    @property
    def fitness(self):
        self.game_state = self.game.game_state
        return self.game_state.fitness_score