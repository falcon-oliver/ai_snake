from collections import deque
import random

from include.game import renderer
from include.game.controls import DOWN, LEFT, RIGHT, UP
from include.game.game_state import GameState

LHS = 0
TOP = 1
RHS = 2
BOTTOM = 3
class Game:

    def __init__(self, game_width, game_height):
        self.snake = deque([(10, 10), (9, 10), (8, 10)])
        self.direction = (1, 0)
        self.snack = None
        self.score = None
        self.game_over = False
        self.game_width = game_width
        self.game_height = game_height
        self.snack = self._snack_spawn()
        self.game_state = GameState(self)


    def _snack_spawn(self):
        while True:
            unique = True
            ran_x = random.randint(0, self.game_width -1)
            ran_y = random.randint(0, self.game_height -1)
            for x,y in self.snake:
                if ran_x == x and ran_y == y:
                    unique = False
                    break
            if unique:
                return (ran_x, ran_y)

    def _handle_direction(self, move):
        if move == UP:
            if self.direction[1] == 0:
                self.direction = (0, -1)
        if move == DOWN:
            if self.direction[1] == 0:
                self.direction = (0, 1)
        if move == LEFT:
            if self.direction[0] == 0:
                self.direction = (-1, 0)
        if move == RIGHT:
            if self.direction[0] == 0:
                self.direction = (1, 0)
        return self.direction

    def _detect_wall_collision(self):
        snake_head = self.snake[0]
        if snake_head[0] < 0 or snake_head[0] >= self.game_width:
            return True
        if snake_head[1] < 0 or snake_head[1] >= self.game_height:
            return True
        return False

    def _detect_self_collision(self):
        snake_head = self.snake[0]
        snake_body = list(self.snake)[1:]
        for x, y in snake_body:
            if snake_head[0] == x and snake_head[1] == y:
                return True
        return False
    
    def _has_collided(self):
        return self._detect_wall_collision() or self._detect_self_collision()
        
    def _ate_snack(self):
        snack_x, snack_y = self.snack
        for segment in self.snake:
            snake_x, snake_y = segment
            if snack_x == snake_x and snack_y == snake_y:
                return True
        return False

    def _move_snake(self):
        snake_head = self.snake[0]
        new_snake_head = (snake_head[0] + self.direction[0], snake_head[1] + self.direction[1])
        self.snake.appendleft(new_snake_head)


    def _init_snake(self):
        bound_x_min = int(self.game_width / 4)
        bound_x_max = int(3 * bound_x_min)

        bound_y_min = int( self.game_height / 4)
        bound_y_max = int(3 * bound_y_min)

        snake_x = random.randint(bound_x_min, bound_x_max)
        snake_y = random.randint(bound_y_min, bound_y_max)

        self.snake = deque([(snake_x, snake_y), (snake_x-1, snake_y), (snake_x-2, snake_y)])
        self.direction = (1, 0)

    def _reset(self):
        self._init_snake()
        self.snack = self._snack_spawn()

    
    def step(self, move):
        reward = 0

        self._handle_direction(move)
        self._move_snake()
        self.game_over = self._has_collided()

        if self.game_over:
            self._reset()
            reward = -1
        else:
            if self._ate_snack():
                self.snack = self._snack_spawn()
                reward = 1
            else:
                reward = 0
                self.snake.pop()

        return self.game_state, reward, self.game_over, self.score
    
