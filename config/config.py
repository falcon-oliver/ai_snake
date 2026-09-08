import yaml
from dataclasses import dataclass

@dataclass
class NetworkWeights:
    weight_ceil: float
    weight_floor: float
    bias_ceil: float
    bias_floor: float
    bias_strength: float

@dataclass
class GeneticAlgorithmConfig:
    candidate_set_size: float
    elite_set_size: float
    crossover_rate: float
    mutation_rate: float
    mutation_strength: float
    snake_games: int
    network_weights: NetworkWeights

@dataclass
class NeuralNetworkConfig:
    hidden_layer: int

@dataclass
class FitnessConfig:
    snack_weight: float
    survival_weight: float
    idle_weight: float
    shaping_reward_weight: float
    collision_penalty: float
    timeout_penalty: float
    inactivity_threshold: int

def load_configs(path):
    config = None
    with open(path) as config_file:
        config = yaml.safe_load(config_file)
    genetic_algorithm_data = config['genetic_algorithm']
    genetic_algorithm_config = GeneticAlgorithmConfig(**genetic_algorithm_data)
    genetic_algorithm_config.network_weights = NetworkWeights(**genetic_algorithm_data['network_weights'])
    return (
        genetic_algorithm_config,
        NeuralNetworkConfig(**config['neural_network']),
        FitnessConfig(**config['fitness'])
    )

genetic_algorithm_config, neural_network_config, fitness_config = load_configs('./config/config.yaml')