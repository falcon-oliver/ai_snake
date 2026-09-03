
import os
import torch

from torch import nn
from torch.utils.data import DataLoader

from include.game.controls import RIGHT
from include.game.game import Game
from include.game.game_state import GameState


'''
    Input: 
    danger forward, right, left
    snack forward, right, left, behind

    hidden: 
    12

    output:
    turn right, turn left, forward
'''
INPUT_LAYER = 7
HIDDEN_LAYER = 12
OUTPUT_LAYER = 3
class NeuralNetwork(nn.Module):

    def __init__(self, game, weights):
        super().__init__()
        self.game = game
        self.game_state = GameState(self.game)
        self.weights = weights

        self.network = nn.Sequential(
            nn.Linear(INPUT_LAYER, HIDDEN_LAYER),
            nn.ReLU(),
            nn.Linear(HIDDEN_LAYER, OUTPUT_LAYER)
        )

    def forward(self, x):


        pass


    def play_game(self):
        while not self.game.game_over:
            self.forward(self.game_state)


    @property
    def fitness(self):

        pass
    
    pass