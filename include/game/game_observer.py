from torch import tensor, float32
from numpy import dot
from config.config import fitness_config

SNACK_WEIGHT = fitness_config.snack_weight
TIME_SURVIVED_WEIGHT = fitness_config.survival_weight
STAGNATION_WEIGHT = fitness_config.idle_weight
SHAPING_REWARD_WEIGHT = fitness_config.shaping_reward_weight
COLLISION_PENALTY = fitness_config.collision_penalty
TIMEOUT_PENALTY = fitness_config.timeout_penalty
INACTIVITY_THRESHOLD = fitness_config.inactivity_threshold

class GameObserver:
    def __init__(self, game):
        self.game = game
        self.game_width = game.game_width
        self.game_height = game.game_height
        self.direction = self.game.direction
        self.snake = self.game.snake
        self.snack = self.game.snack
        self.snacks_ate = 0
        self.time_survived = 0
        self.shaping_reward = 0
        self.previous_distance = self.snack_distance
        self.inactivity = 0
        self.collision = False
        self.moves_since_snack = 0

    def _handle_snack_status(self, snack_ate):
        if snack_ate:
            self.snacks_ate += 1
            self.moves_since_snack = 0
        else:
            self.moves_since_snack += 1

    def _handle_inactivity_status(self):
        if self.moves_since_snack >= INACTIVITY_THRESHOLD:
            self.inactivity += 1

    def _handle_shaping_status(self, distance):
        if distance < self.previous_distance:
            self.shaping_reward += abs(self.previous_distance - distance)
        else:
            self.shaping_reward -= abs(distance - self.previous_distance)
        self.previous_distance = distance

    def _handle_survival_status(self, timeout, collision):
        self.collision = collision
        self.timeout = timeout
        if not collision and not timeout:
            self.time_survived += 1

    def refresh_state(self):
        self.direction = self.game.direction
        self.snake = self.game.snake
        self.snack = self.game.snack

    def update_state(self, step_data):
        snack_ate, timeout, collision = step_data
        distance = self.snack_distance
        self._handle_snack_status(snack_ate)
        self._handle_inactivity_status()
        if not snack_ate:
            self._handle_shaping_status(distance)

        self._handle_survival_status(timeout, collision)

    def _rotate_right(self, direction):
        dx, dy = direction
        right = (-dy, dx)
        return right

    def _rotate_left(self, direction):
        dx, dy = direction
        left = (dy, -dx)
        return left

    def _danger_distance(self, direction):
        dx, dy = direction
        x, y = self.snake[0]
        distance = 0
        while True:
            x += dx
            y += dy
            distance += 1
            if x < 0 or x >= self.game_width or y < 0 or y >= self.game_height:
                return distance / max(self.game_width, self.game_height)
            if (x, y) in self.snake:
                return distance / max(self.game_width, self.game_height)
    
    def _snack_distance(self, direction):
        snake_x, snake_y = self.snake[0]
        snack_x, snack_y = self.snack
        snack_distance = (snack_x - snake_x, snack_y - snake_y)
        distance = dot( snack_distance, direction )
        distance /= (self.game_width + self.game_height)
        return distance

    def _snack_direction(self, direction):
        snake_x, snake_y = self.snake[0]
        snack_x, snack_y = self.snack
        dx, dy = snack_x - snake_x, snack_y - snake_y
        norm = (dx*dx + dy*dy) ** 0.5 or 1.0
        return dot((dx / norm, dy / norm), direction)
    
    @property
    def danger_forward_distance(self):
        return self._danger_distance(self.direction)

    @property
    def danger_left_distance(self):
        return self._danger_distance(self._rotate_left(self.direction))

    @property
    def danger_right_distance(self):
        return self._danger_distance(self._rotate_right(self.direction))
    
    @property
    def snack_forward_distance(self):
        return self._snack_distance(self.direction)

    @property
    def snack_left_distance(self):
        return self._snack_distance(self._rotate_left(self.direction))

    @property
    def snack_distance(self):
        snake_x, snake_y = self.snake[0]
        snack_x, snack_y = self.snack
        return abs(snake_x - snack_x) + abs(snake_y - snack_y)

    @property
    def snack_forward_direction(self):
        return self._snack_direction(self.direction)

    @property
    def snack_left_direction(self):
        return self._snack_direction(self._rotate_left(self.direction))

    @property
    def snack_right_direction(self):
        return self._snack_direction(self._rotate_right(self.direction))

    @property
    def snack_proximity(self):
        return 1.0 / (1.0 + self.snack_distance)

    @property
    def state(self):
        self.refresh_state()
        return tensor([
                self.danger_forward_distance, 
                self.danger_left_distance, 
                self.danger_right_distance, 
                self.snack_forward_direction, 
                self.snack_left_direction,
                self.snack_right_direction
        ], dtype=float32)

    @property
    def fitness_score(self):
        penalty = COLLISION_PENALTY if self.collision else TIMEOUT_PENALTY
        fitness_score = ( 
             (self.snacks_ate * SNACK_WEIGHT)
            + (self.time_survived * TIME_SURVIVED_WEIGHT)
            + (self.shaping_reward * SHAPING_REWARD_WEIGHT)
            - (self.inactivity * STAGNATION_WEIGHT)
            - (penalty)
        )
        return fitness_score
