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
        self.game_state = GameState(self.snake, self.snack, self.score)
        pass


    def _snack_spawn(self):
        ran_x = random.randint(0, self.game_width -1)
        ran_y = random.randint(0, self.game_height -1)
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
        pass


    def _init_snake(self):
        bound_x_min = int(self.game_width / 4)
        bound_x_max = int(3 * bound_x_min)

        bound_y_min = int( self.game_height / 4)
        bound_y_max = int(3 * bound_y_min)

        snake_x = random.randint(bound_x_min, bound_x_max)
        snake_y = random.randint(bound_y_min, bound_y_max)

        self.snake = deque([(snake_x, snake_y), (snake_x-1, snake_y), (snake_x-2, snake_y)])
        self.direction = (1, 0)
        pass

    def _init_snack(self):

        '''
            the only comment necessary, but, the snake spawns in a centre box
            and the food spawns outside of it. the lhs, top, rhs or bottom. 
            a random number between 0-3 will determine the area to spawn in.
        '''

        bound_selection = random.randint(0, 3)

        bound_x_max = bound_x_min = bound_y_max = bound_y_min = 0

        if bound_selection == LHS:
            bound_x_min = 0
            bound_x_max = int(self.game_width / 4) -1      

            bound_y_min = 0
            bound_y_max = self.game_height
            pass
        if bound_selection == TOP:
            bound_x_min = 0
            bound_x_max = self.game_width

            bound_y_min = 0
            bound_y_max = int( self.game_height / 4) - 1

            pass

        if bound_selection == RHS:
            bound_x_min = 3 * int(self.game_width / 4)
            bound_x_max = self.game_width

            bound_y_min = 0
            bound_y_max = self.game_height
            pass

        if bound_selection == BOTTOM:
            bound_x_min = 0
            bound_x_max = self.game_width

            bound_y_min = 3 * int(self.game_height / 4) +1
            bound_y_max = self.game_height

            pass


        snack_x = random.randint(bound_x_min, bound_x_max)
        snack_y = random.randint(bound_y_min, bound_y_max)
        self.snack = (snack_x, snack_y)
        pass
    
    def _reset(self):
        self._init_snake()
        self._init_snack()
        pass

    
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

        self.game_state = GameState(self.snake, self.snack, self.score)

        return self.game_state, reward, self.game_over, self.score
    
    pass