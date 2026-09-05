from torch import tensor, float32, inf
from numpy import dot

SNACK_WEIGHT = 10
TIME_SURVIVED_WEIGHT = 0.00
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
                return distance
            
            if (x, y) in self.snake:
                return distance
    
    def _snack_distance(self, direction):
        snake_x, snake_y = self.snake[0]
        snack_x, snack_y = self.snack
        snack_distance = (snack_x - snake_x, snack_y - snake_y)
        distance = dot( snack_distance, direction )
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
    def snack_right_distance(self):
        return self._snack_distance(self._rotate_right(self.direction))

    @property
    def snack_behind_distance(self):
        dx, dy = self.direction
        behind = (-dx, -dy)
        return self._snack_distance(behind)

    @property
    def game_state(self):
        self.direction = self.game.direction
        self.snake = self.game.snake
        self.snack = self.game.snack
        return tensor([self.danger_forward_distance, self.danger_left_distance, self.danger_right_distance, self.snack_forward_distance, self.snack_left_distance, self.snack_right_distance, self.snack_behind_distance], dtype=float32)

    @property
    def fitness_score(self):
        fitness_score = self.snacks_ate * SNACK_WEIGHT + self.time_survived * TIME_SURVIVED_WEIGHT
        return fitness_score
        