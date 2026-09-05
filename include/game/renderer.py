import pygame

FPS = 60
BACKGROUND = (255, 255, 255)
GRID_LINE = (150, 150, 150)
SNAKE = (0, 0, 0)
SNACK = (150, 0, 0)
class Renderer:
    def __init__(self, game_width, game_height, window_width, window_height):
        self.screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("snake gen algorithm")
        self.game_width = game_width
        self.game_height = game_height
        self.window_width = window_width
        self.window_height = window_height
        self.cell_width =  int(window_width / game_width)
        self.cell_height = int(window_height / game_height)
        self.render_clock = pygame.time.Clock()
        pass

    def _render_background(self):
        self.screen.fill(BACKGROUND)
        for x in range(0, self.window_width, self.cell_width):
            pygame.draw.line(self.screen, GRID_LINE, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_height):
            pygame.draw.line(self.screen, GRID_LINE, (0, y), (self.window_width, y))

    def _draw_snake(self, game_state):
        snake = game_state.snake
        for x, y in snake:
            pygame.draw.rect(self.screen, SNAKE, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))

    def _draw_snack(self, game_state):
        snack = game_state.snack
        x, y = snack
        pygame.draw.rect(self.screen, SNACK, (x*self.cell_width, y*self.cell_height, self.cell_width, self.cell_height))

    def _print_inline(self, text):
        print(f"\r{text}", end="", flush=True)

    def _print_state(self, game_state):
        tensor = game_state.game_state
        (danger_forward_distance, danger_left_distance, danger_right_distance, snack_forward_distance, snack_left_distance, snack_right_distance, snack_behind_distance) = tensor
        danger_forward = f"d fwd: {danger_forward_distance}"
        danger_left = f"d lft: {danger_left_distance}"
        danger_right = f"d rgt: {danger_right_distance}"

        snack_forward = f"s fwd: {snack_forward_distance}"
        snack_left = f"s left: {snack_left_distance}"
        snack_right = f"s rgt: {snack_right_distance}"
        snack_behind = f"s bhd: {snack_behind_distance}"

        self._print_inline(f"{danger_forward} | {danger_left} | {danger_right} | {snack_forward} | {snack_left} | {snack_right} | {snack_behind}")


    def _render_game(self, game_state):
        self._draw_snake(game_state)
        self._draw_snack(game_state)
        self._print_state(game_state)
    
    def render(self, game_state):
        self._render_background()
        self._render_game(game_state)
        pygame.display.flip()
        self.render_clock.tick(FPS)

    def quit(self):
        pygame.quit()