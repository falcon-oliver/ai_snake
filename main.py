from include.ai.genetic_algorithm import GeneticAlgorithm
from include.ai.neural_network import NeuralNetwork
from include.game.game import Game
from include.game.handle_input import InputHandler
from include.game.renderer import Renderer

FPS = 60
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
        if frames >= FPS:
            frames = 0

def train_play(iterations):
    print("Training...")
    game = Game(game_width, game_height)

    gen_algorithm = GeneticAlgorithm(game_width, game_height, start_population_count=1000)
    neural_network = gen_algorithm.train(iterations)
    renderer = Renderer(game_width, game_height, window_width, window_height)

    while True:
        game_state = game.game_state
        current_move = 1
        game.step(current_move)
        renderer.render(game_state)    


if __name__ == "__main__":

    play = True
    gen_count = 250

    game_width = 70
    game_height = 70

    window_width = game_width * 10
    window_height = game_height * 10

    iterations = 500


    if play:
        play_game()
    else:
        train_play(iterations)