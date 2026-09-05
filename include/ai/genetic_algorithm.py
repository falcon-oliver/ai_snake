


import random
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game
import torch

CANDIDATE_SET = 10
ELITE_SET = 10
class GeneticAlgorithm:

    def __init__(self, game_width, game_height, start_population_count=1000):
        self.start_population_count = start_population_count
        self.candidate_len = int(start_population_count / CANDIDATE_SET)
        self.elite_len = int(self.candidate_len / ELITE_SET)
        self.game_width = game_width
        self.game_height = game_height
        self.optimal_network = None
        
    def _generate_start_population(self):
        start_population = []
        for i in range(self.start_population_count):
            game = Game(self.game_width, self.game_height)
            neural_network = NeuralNetwork(game)
            neural_network.generate_random_weights()
            start_population.append(neural_network)
        return start_population

    def _evaluate(self, neural_network):
        neural_network.play_game()
        fitness = neural_network.fitness
        return fitness


    def _get_candidate_set(self, fitness_scores, population):
        return self._get_top_k(fitness_scores, population, self.candidate_len)

    def _get_elite_set(self, fitness_scores, population):
        return self._get_top_k(fitness_scores, population, self.elite_len)

    def _get_top_k(self, fitness_scores, population, k):
        _, indicies = torch.topk(torch.tensor(fitness_scores), k)
        k = [population[j] for j in indicies]
        return k

    def _evaluate_population(self, population):
        fitness_scores = []
        for neural_network in population:
            fitness_score = self._evaluate(neural_network)
            fitness_scores.append(fitness_score)

        return fitness_scores

    def train(self, iterations=1000):
        population = self._generate_start_population()
        for i in range(iterations):
            fitness_scores = self._evaluate_population(population)
            candidates = self._get_candidate_set(fitness_scores, population)
            elites = self._get_elite_set(fitness_scores, population)
            population = self._generate_new_population(candidates, elites)

        fitness_scores = self._evaluate_population(population)
        _, index = self.optimal_network = torch.topk(torch.tensor(fitness_scores), 1)
        self.optimal_network = population[index]

    def get_network(self):
        return self.optimal_network

    def _generate_new_population(self, candidates, elites):
        new_candidates = []

        return candidates


    def _crossover(self, network_a, network_b):


        pass


    

    pass