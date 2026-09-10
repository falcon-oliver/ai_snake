# Neurogenetic algorithm for Snake game

<p align="center">
<img width="500" height="491" alt="snake" src="https://github.com/user-attachments/assets/6e18aaf7-6c55-4474-9d1b-e05549b88f0b" />
</p>

# Install
```bash
git clone https://github.com/falcon-oliver/ai_snake.git
cd ai_snake
pip install -r requirements.txt
```


# Usage

Default train and test model. <code>iterations=20 start_population=100</code>
```bash
python3 main.py
```

Save model
```bash
python3 main.py -s ./models/out.pt
```

Load model
```bash
python3 main.py -l ./models/example.pt
```

Play the game
```bash
python3 main.py -t
```

Change iterations
```bash
python3 main.py -i 100
```

Change start population
```bash
python3 main.py -p 200
```
# Configuration

Tunable values found in <code>config/config.yaml</code>

## Genetic algorithm configuration
| Variable | Purpose | Default value |
| --- | --- | --- |
| candidate_set_size | The size of the candidate set to take from the current population | 0.5 |
| elite_set_size | The size of the elite set to take from the current population | 0.1 |
| crossover_rate | The rate of crossover between two candidates | 0.5 |
| mutation_rate | The mutation rate of both the weights and the bias | 0.1 |
| weight_mutation_strength | The strength of mutation for the weights | 0.15 |
| bias_mutation_strength | The strength of mutation for the bias | 0.1 |
| snake_games | The amount of snake games each candidate has to play before working out the average fitness score | 0.5 |



## Neural network configuration
| Variable | Purpose | Default value |
| --- | --- | --- |
| hidden_layer | The size of the hidden layer in the neural networks | 7 |
| weight_ceil | The maximum value of a neural network weight | 1 |
| weight_floor | The minimum value of a neural network weight | -1 |
| bias_ceil | The maximum value of a neural network bias | 0.5 |
| bias_floor | The minimum value of a neural network bias | -0.5 |

## Fitness configuration
| Variable | Purpose | Default value |
| --- | --- | --- |
| snack_weight | Weight for the snacks eaten | 100 |
| survival_weight | Weight for each frame survived | 0.1 |
| idle_weight | Inactivity weight | 0 |
| shaping_reward_weight | Weight for moving toward the snack each frame | 1 |
| collision_penalty | Penalty for self collision or wall collision | 70 |
| timeout_penalty | Penalty for losing to timeout | 40 |
| inactivity_threshold | How many moves without a snack before it's classed as inactive | 40 |


## Game configuration
| Variable | Purpose | Default value |
| --- | --- | --- |
| timeout_limit | The number of moves since collecting a snack before timing out | 70 |
| timeout_bonus | The number of additional moves added to timeout_limit after collecting a snack | 10 |


# Technical details

## Fitness function

```math

\text{snacks\_ate}=\alpha,~
\text{time\_survived}=\beta,~
\text{shaping\_reward}=\gamma,~
\text{inactivity}=\delta,~
\text{penalty}=\epsilon,~
\text{weights}=\omega_n
```


```math
fitness=\frac{\sum_{j=0}^{n} \alpha * \omega_1 + \beta *\omega_2 + \gamma *\omega_3 - \delta * \omega_4 - \epsilon }{n}
```

