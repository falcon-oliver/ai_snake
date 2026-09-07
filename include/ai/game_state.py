from torch import tensor, float32, inf
from numpy import dot

SNACK_WEIGHT = 100
TIME_SURVIVED_WEIGHT = 0.1
STAGNATION_WEIGHT = 0
SHAPING_REWARD_WEIGHT = 1.0
COLLISION_PENALTY = 400
TIMEOUT_PENALTY = 400

class GameState:
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
        self.inactivity = 0
        self.collision = False

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

    def _snack_direction(self, direction):
        snake_x, snake_y = self.snake[0]
        snack_x, snack_y = self.snack
        dx, dy = snack_x - snake_x, snack_y - snake_y
        norm = (dx*dx + dy*dy) ** 0.5 or 1.0
        return dot((dx / norm, dy / norm), direction)

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
    def game_state(self):
        self.direction = self.game.direction
        self.snake = self.game.snake
        self.snack = self.game.snack
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
