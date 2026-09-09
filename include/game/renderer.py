import pygame
FPS = 60
BACKGROUND = (0, 0, 0)
GRID_LINE = (40, 40, 40)
SNAKE = (0, 255, 0)
SNACK = (255, 0, 0)
class Renderer:
    def __init__(self, game_width, game_height, window_width, window_height):
        pygame.init()
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("ai_snake")
        self.game_width = game_width
        self.game_height = game_height
        self.window_width = window_width
        self.window_height = window_height
        self.cell_width =  int(window_width / game_width)
        self.cell_height = int(window_height / game_height)
        self.render_clock = pygame.time.Clock()

    def _render_background(self):
        self.screen.fill(BACKGROUND)
        for x in range(0, self.window_width, self.cell_width):
            pygame.draw.line(self.screen, GRID_LINE, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_height):
            pygame.draw.line(self.screen, GRID_LINE, (0, y), (self.window_width, y))

    def _draw_snake(self, state):
        snake = state.snake
        for x, y in snake:
            pygame.draw.rect(self.screen, SNAKE, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))

    def _draw_snack(self, state):
        snack = state.snack
        x, y = snack
        pygame.draw.rect(self.screen, SNACK, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))

    def _check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def render(self, state):
        self._render_background()
        self._draw_snake(state)
        self._draw_snack(state)
        self._check_quit()
        pygame.display.flip()
        self.render_clock.tick(FPS)
