import typer
import random
import json

from src.modles import HangmanGame
from src.utils import system_printer

app: typer.Typer = typer.Typer()


@app.command()
def start():
    while True:
        try:
            n = int(typer.prompt("Enter the number of players"))
            if n <= 0:
                raise ValueError("Number of players must be a positive integer.")
            break
        except ValueError as e:
            system_printer(f"Invalid input: {e}. Please enter a valid number of players.")

    with open('words.json', 'r') as f:
        data: dict = json.load(f)
        words: list[str] = data["words"][:15]  # get only the first 15 words

    word: str = random.choice(words)

    players: list[str] = [f"Player {i + 1}" for i in range(n)]

    system_printer("Welcome to Hangman!")
    system_printer("Try to guess the word one letter at a time.")

    guesses_count: int = 20

    game: HangmanGame = HangmanGame(word, players, guesses_count)

    while not game.is_finished():
        game.display()
        current_player: str = game.players[game.current_player_index]

        system_printer(f"It's {current_player}'s turn.")

        guess: str = typer.prompt("Enter your guess")
        if len(guess) != 1 or not guess.isalpha():
            system_printer("Invalid input. Please enter a single letter.")
            continue
        correct: bool = game.guess(current_player, guess)

        if not correct:
            full_word_guess: str = typer.prompt("Guess the entire word or press 'skip' to skip")
            if full_word_guess == 'skip':
                system_printer("skipping")
                game.next_player()
            elif full_word_guess and full_word_guess.lower() == game.word:
                missing_letters: int = game.guessed_word.count('_')
                game.scores[current_player] += missing_letters
                game.guessed_word = list(game.word)
                system_printer(f"Correct! {current_player} guessed the word and earned {missing_letters} points.")
            else:
                system_printer("Nope, next player please")

                game.next_player()

        elif correct:
            system_printer(f"{current_player} guessed correctly and gets another turn.")

    system_printer(game.get_result())


if __name__ == "__main__":
    app()
