import yaml
from dataclasses import dataclass


@dataclass
class GeneticAlgorithmConfig:
    candidate_set_size: float
    elite_set_size: float
    crossover_rate: float
    mutation_rate: float
    weight_mutation_strength: float
    bias_mutation_strength: float
    snake_games: int

@dataclass
class NeuralNetworkConfig:
    hidden_layer: int
    weight_ceil: float
    weight_floor: float
    bias_ceil: float
    bias_floor: float

@dataclass
class FitnessConfig:
    snack_weight: float
    survival_weight: float
    idle_weight: float
    shaping_reward_weight: float
    collision_penalty: float
    timeout_penalty: float
    inactivity_threshold: int

@dataclass
class GameConfig:
    timeout_limit: int
    timeout_bonus: int

def load_configs(path):
    config = None
    with open(path) as config_file:
        config = yaml.safe_load(config_file)
    return (
        GeneticAlgorithmConfig(**config['genetic_algorithm']),
        NeuralNetworkConfig(**config['neural_network']),
        FitnessConfig(**config['fitness']),
        GameConfig(**config['game'])
    )

genetic_algorithm_config, neural_network_config, fitness_config, game_config = load_configs('./config/config.yaml')