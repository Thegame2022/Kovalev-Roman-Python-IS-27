# main.py
from gonki import reset_game

def start_game():
    print("Запуск игры...")
    game = reset_game()
    game.run()

if __name__ == "__main__":
    start_game()