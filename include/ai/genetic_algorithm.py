import random
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game
from config.config import genetic_algorithm_config
import torch

CANDIDATE_SET = genetic_algorithm_config.candidate_set_size
ELITE_SET = genetic_algorithm_config.elite_set_size
MUTATION_RATE = genetic_algorithm_config.mutation_rate
MUTATION_STRENGTH = genetic_algorithm_config.mutation_strength
CROSSOVER_RATE = genetic_algorithm_config.crossover_rate
SNAKE_GAMES = genetic_algorithm_config.snake_games
WEIGHT_FLOOR = genetic_algorithm_config.network_weights.weight_floor
WEIGHT_CEIL = genetic_algorithm_config.network_weights.weight_ceil
BIAS_STRENGTH = genetic_algorithm_config.network_weights.bias_strength
BIAS_FLOOR = genetic_algorithm_config.network_weights.bias_floor
BIAS_CEIL = genetic_algorithm_config.network_weights.bias_ceil

class GeneticAlgorithm:

    def __init__(self, game_width, game_height, start_population_count=1000):
        self.start_population_count = start_population_count
        self.candidate_len = max(2, int(start_population_count * CANDIDATE_SET))
        self.elite_len = max(1, int(start_population_count * ELITE_SET))
        self.game_width = game_width
        self.game_height = game_height
        self.optimal_network = None

    def train(self, iterations=1000):
        population = self._generate_random_population(self.start_population_count)
        for i in range(iterations):
            fitness_scores = self._evaluate_population(population)
            fittest_candidate_index = fitness_scores.index(max(fitness_scores))
            print(f'MAX_FITNESS={fitness_scores[fittest_candidate_index]:.2f}\t\tEPOCH={i}/{iterations}')
            candidates = self._get_candidate_set(fitness_scores, population)
            elites = self._get_elite_set(fitness_scores, population)
            population = self._generate_new_population(candidates, elites)
        fitness_scores = self._evaluate_population(population)
        fittest_candidate_index = fitness_scores.index(max(fitness_scores))
        print(f'MAX_FITNESS={fitness_scores[fittest_candidate_index]:.2f}\t\tEPOCH={iterations}/{iterations}')
        self.optimal_network = population[fittest_candidate_index]

    def get_network(self):
        return self.optimal_network

    def _generate_random_population(self, population_count):
        population = []
        for i in range(population_count):
            game = Game(self.game_width, self.game_height)
            neural_network = NeuralNetwork(game)
            population.append(neural_network)
        return population

    def _evaluate(self, neural_network):
        scores = 0
        for i in range(SNAKE_GAMES):
            neural_network.play_game()
            fitness = neural_network.fitness
            scores += fitness
        scores /= SNAKE_GAMES
        return scores

    def _evaluate_population(self, population):
        fitness_scores = []
        for neural_network in population:
            fitness_score = self._evaluate(neural_network)
            fitness_scores.append(fitness_score)
        return fitness_scores

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
            mutated_weights = self._mutate_weights(candidate)
            mutated_bias = self._mutate_bias(candidate)
            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(mutated_weights)
            new_candidate.load_bias(mutated_bias)
            mutated_candidates.append(new_candidate)
        return mutated_candidates

    def _mutate_param(self, param, mutation_strength, param_ceil, param_floor):
        mask = torch.rand_like(param) < MUTATION_RATE
        noise = (torch.rand_like(param) * 2 - 1) * mutation_strength
        mutated_bias = torch.where(mask, param + noise, param)
        return torch.clamp(mutated_bias, param_floor, param_ceil)

    def _crossover_param(self, param_a, param_b):
        mask = torch.rand_like(param_a) < CROSSOVER_RATE
        crossover = torch.where(mask, param_a, param_b)
        return crossover
    
    def _crossover(self, candidates):
        crossovers = []
        for i in range(1, len(candidates)):
            parent_a = candidates[i-1]
            parent_b = candidates[i]
            crossover_weights = self._crossover_weight(parent_a, parent_b)
            crossover_bias = self._crossover_bias(parent_a, parent_b)
            new_candidate = NeuralNetwork(Game(self.game_width, self.game_height))
            new_candidate.load_weights(crossover_weights)
            new_candidate.load_bias(crossover_bias)
            crossovers.append(new_candidate)        
        return crossovers

    def _crossover_bias(self, parent_a, parent_b):
        return self._crossover_param(parent_a.get_bias(), parent_b.get_bias())
    
    def _crossover_weight(self, parent_a, parent_b):
        return self._crossover_param(parent_a.get_weights(), parent_b.get_weights())

    def _mutate_bias(self, candidate):
        return self._mutate_param(candidate.get_bias(), BIAS_STRENGTH, BIAS_CEIL, BIAS_FLOOR)

    def _mutate_weights(self, candidate):
        return self._mutate_param(candidate.get_weights(), MUTATION_STRENGTH, WEIGHT_CEIL, WEIGHT_FLOOR)
    
    def _get_candidate_set(self, fitness_scores, population):
        return self._get_top_k(fitness_scores, population, self.candidate_len)

    def _get_elite_set(self, fitness_scores, population):
        return self._get_top_k(fitness_scores, population, self.elite_len)

    def _get_top_k(self, fitness_scores, population, k):
        _, indicies = torch.topk(torch.tensor(fitness_scores), k)
        k = [population[j] for j in indicies]
        return k