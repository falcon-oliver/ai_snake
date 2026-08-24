from include.game.game import Game
from include.game.handle_input import InputHandler
from include.game.renderer import Renderer

def play_game():
    frames = 0
    renderer = Renderer(game_width, game_height, window_width, window_height)
    game = Game(game_width, game_height)
    input_handler = InputHandler()

    while True:
        frames += 1
        if frames % 30 == 0:
            game_state = game.game_state
            current_move = input_handler.get_move()
            game.step(current_move)
            renderer.render(game_state)
        if frames >= 60:
            frames = 0


def train_play(iterations):


    pass

if __name__ == "__main__":

    play = True
    gen_count = 250

    game_width = 70
    game_height = 70

    window_width = game_width * 10
    window_height = game_height * 10

    if play:
        play_game()
    else:
        train_play()