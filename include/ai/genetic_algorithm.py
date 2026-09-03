


import random
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game

WEIGHT_CEIL = 5
WEIGHT_FLOOR = -5
class GeneticAlgorithm:

    def __init__(self, game_width, game_height, start_population_count=1000):
        self.start_population_count = start_population_count
        self.game_width = game_width
        self.game_height = game_height
        self.optimal_network = None
        pass

    def _random_weight(self):
        return random.uniform(WEIGHT_FLOOR, WEIGHT_CEIL)
    
    def _generate_random_weights(self):
        danger_source = self._random_weight()
        food_distance = self._random_weight()
        return [danger_source, food_distance]
    
    def _generate_start_population(self):
        start_population = []
        for i in range(self.start_population_count):
            weights = self._generate_random_weights()
            game = Game(self.game_width, self.game_height)
            neural_network = NeuralNetwork(game, weights)
            start_population.append(neural_network)
        return start_population

    def _evaluate(self, neural_network):
        neural_network.play_game()
        fitness = neural_network.fitness
        return fitness

    def train(self, epochs=1000):

        '''
            generate game instances
            generate start population
            train against the game
            take best algorithms
            restart n times
        '''
        population = self._generate_start_population()
        for i in range(epochs):
            for neural_network in population:
                fitness_score = self._evaluate(neural_network)
                
                pass

            


            pass

            


        

        pass

    def crossover(self):


        pass

    def step(self, game):

        if self.optimal_network is None:
            print("train.")

        pass
    

    pass