from math import hypot


class GameState:
    def __init__(self, game):
        self.game = game
        pass

    @property
    def snake(self):
        return self.game.snake
    @property
    def snack(self):
        return self.game.snack

    @property
    def snack_distance(self):
        head_x, head_y = self.game.snake[0]
        snack_x, snack_y = self.game.snack
        return hypot(snack_x - head_x, snack_y - head_y)

    @property
    def wall_left_distance(self):
        head_x, _ = self.game.snake[0]
        return head_x

    @property
    def wall_right_distance(self):
        head_x, _ = self.game.snake[0]
        return self.game.game_width - head_x
    
    @property 
    def wall_top_distance(self):
        _, head_y = self.game.snake[0]
        return head_y

    @property
    def wall_bottom_distance(self):
        _, head_y = self.game.snake[0]
        return self.game.game_height - head_y

    @property
    def game_state(self):
        return self.snack_distance, self.wall_left_distance, self.wall_right_distance, self.wall_top_distance, self.wall_top_distance


    @property
    def fitness_score(self):
        fitness_score = 0
        return fitness_score
