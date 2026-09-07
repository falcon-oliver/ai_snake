


import random
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game
import torch

CANDIDATE_SET = 0.5
ELITE_SET = 0.15
MUTATION_RATE = 0.1
MUTATION_STRENGTH = 0.15
CROSSOVER_RATE = 0.5
WEIGHT_FLOOR = -1
WEIGHT_CEIL = 1
GAMES_PLAYED = 7
BIAS_STRENGTH = 0.1
BIAS_FLOOR = -0.5
BIAS_CEIL = 0.5
class GeneticAlgorithm:

    def __init__(self, game_width, game_height, start_population_count=1000):
        self.start_population_count = start_population_count
        self.candidate_len = max(2, int(start_population_count * CANDIDATE_SET))
        self.elite_len = max(1, int(start_population_count * ELITE_SET))
        self.game_width = game_width
        self.game_height = game_height
        self.optimal_network = None

    def _generate_random_population(self, population_count):
        population = []
        for i in range(population_count):
            game = Game(self.game_width, self.game_height)
            neural_network = NeuralNetwork(game)
            population.append(neural_network)
        return population

    def _evaluate(self, neural_network):
        scores = 0
        for i in range(GAMES_PLAYED):
            neural_network.play_game()
            fitness = neural_network.fitness
            scores += fitness
        scores /= GAMES_PLAYED
        return scores

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
            fitness_scores = self._evaluate_population(population)
            candidates = self._get_candidate_set(fitness_scores, population)
            elites = self._get_elite_set(fitness_scores, population)
            population = self._generate_new_population(candidates, elites)
            fittest_candidate_index = fitness_scores.index(max(fitness_scores))
            print(f'MAX_FITNESS={fitness_scores[fittest_candidate_index]:.2f}\t\tEPOCH={i}/{iterations}')

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
        other_candidates = []

        while len(other_candidates) < rem_pop:
            random_candidates = candidates[:]
            random.shuffle(random_candidates)
            random_candidates = self._crossover(random_candidates)
            random_candidates = self._mutate_candidates(random_candidates)
            other_candidates.extend(random_candidates)

        other_candidates = other_candidates[:rem_pop]

        new_generation.extend(other_candidates)
        
        return new_generation

    def _mutate_candidates(self, candidates):
        mutated_candidates = []
        for candidate in candidates:
            mutated_weights = self._mutate(candidate)
            mutated_bias = self._mutate_bias(candidate)
            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(mutated_weights)
            new_candidate.load_bias(mutated_bias)
            mutated_candidates.append(new_candidate)
        return mutated_candidates

    def _mutate_bias(self, candidate):
        bias = candidate.get_bias()
        mask = torch.rand_like(bias) < MUTATION_RATE
        noise = (torch.rand_like(bias) * 2 - 1) * BIAS_STRENGTH
        mutated_bias = torch.where(mask, bias + noise, bias)
        return torch.clamp(mutated_bias, BIAS_FLOOR, BIAS_CEIL)

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

            bias_mask =  torch.rand_like(parent_a.get_bias()) < CROSSOVER_RATE
            mutated_bias = torch.where(bias_mask, parent_a.get_bias(), parent_b.get_bias())

            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(mutated_weights)
            new_candidate.load_bias(mutated_bias)
            crossovers.append(new_candidate)        
        return crossovers
