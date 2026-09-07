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
    frames = 0
    game = Game(game_width, game_height)
    gen_algorithm = GeneticAlgorithm(game_width, game_height, start_population_count=100)
    gen_algorithm.train(iterations)
    neural_network = gen_algorithm.optimal_network

    renderer = Renderer(game_width, game_height, window_width, window_height)

    while True:
        frames += 1
        if frames % 30 == 0:
            game_state = game.game_state
            current_move = neural_network.get_move(game_state)
            game.test_ai_step(current_move)
            renderer.render(game_state)
        if frames >= FPS:
            frames = 1

if __name__ == "__main__":

    play = False

    game_width = 20
    game_height = 20

    window_width = game_width * 10
    window_height = game_height * 10

    iterations = 50

    if play:
        play_game()
    else:
        train_play(iterations)