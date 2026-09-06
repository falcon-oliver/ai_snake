


import random
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game
import torch

CANDIDATE_SET = 20
ELITE_SET = 10
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 0.05
CROSSOVER_RATE = 0.5
WEIGHT_FLOOR = -1
WEIGHT_CEIL = 1
class GeneticAlgorithm:

    def __init__(self, game_width, game_height, start_population_count=1000):
        self.start_population_count = start_population_count
        self.candidate_len = int(start_population_count / CANDIDATE_SET)
        self.elite_len = int(self.candidate_len / ELITE_SET)
        self.game_width = game_width
        self.game_height = game_height
        self.optimal_network = None

    def _generate_random_population(self, population_count):
        population = []
        for i in range(population_count):
            game = Game(self.game_width, self.game_height)
            neural_network = NeuralNetwork(game)
            neural_network.generate_random_weights()
            population.append(neural_network)
        return population

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
        population = self._generate_random_population(self.start_population_count)
        for i in range(iterations):
            print(f'{i} / {iterations}')
            fitness_scores = self._evaluate_population(population)
            candidates = self._get_candidate_set(fitness_scores, population)
            elites = self._get_elite_set(fitness_scores, population)
            candidates = [candidate for candidate in candidates if candidate not in elites]
            old_population = population
            population = self._generate_new_population(candidates, elites)

            fittest_candidate_index = fitness_scores.index(max(fitness_scores))
            print(f'fittest {old_population[fittest_candidate_index].fitness}')

        fitness_scores = self._evaluate_population(population)
        fittest_candidate_index = fitness_scores.index(max(fitness_scores))
        self.optimal_network = population[fittest_candidate_index]

    def get_network(self):
        return self.optimal_network

    def _generate_new_population(self, candidates, elites):
        new_generation = []


        new_candidates = self._crossover(candidates)
        mutated_candidates = self._mutate_candidates(new_candidates)


        new_generation.extend(mutated_candidates)
        new_generation.extend(elites)

        rem_pop = self.start_population_count - len(mutated_candidates) - len(elites)
        remainder = self._generate_random_population(rem_pop)

        new_generation.extend(remainder)

        return new_generation

    def _mutate_candidates(self, candidates):
        mutated_candidates = []
        for candidate in candidates:
            mutated_weights = self._mutate(candidate)
            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(mutated_weights)
            mutated_candidates.append(new_candidate)
        return mutated_candidates

    def _mutate(self, candidate):
        weights = candidate.get_weights()
        mask = torch.rand_like(weights) < MUTATION_RATE
        noise = (torch.rand_like(weights) * 2 - 1) * MUTATION_STRENGTH
        mutated_weights = torch.where(mask, weights + noise, weights)
        return torch.clamp(mutated_weights, WEIGHT_FLOOR, WEIGHT_CEIL)
    
    def _crossover(self, candidates):
        crossovers = []
        for i in range(1, len(candidates)):
            parent_a = candidates[i-1]
            parent_b = candidates[i]
            mask = torch.rand_like(parent_a.get_weights()) < CROSSOVER_RATE
            mutated_weights = torch.where(mask, parent_a.get_weights(), parent_b.get_weights())
            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(mutated_weights)
            crossovers.append(new_candidate)
        
        return crossovers

