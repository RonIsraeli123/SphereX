class HangmanGame:
    def __init__(self, word: str, players: list[str], guesses_count: int):
        self.word: str = word.lower()
        self.guessed_word: list[str] = ['_'] * len(word)
        self.guessed_letters: set = set()
        self.remaining_guesses: int = guesses_count
        self.scores: dict[str, int] = {player: 0 for player in players}
        self.players: list[str] = players
        self.current_player_index: int = 0

    def guess(self, player: str, letter: str) -> bool:
        letter: str = letter.lower()
        if letter in self.guessed_letters:
            print(f"You have already guessed the letter {letter}. Try again.")
            return False

        self.guessed_letters.add(letter)

        if letter in self.word:
            print(f"Good guess! The letter {letter} is in the word.")
            for i, char in enumerate(self.word):
                if char == letter:
                    self.guessed_word[i] = letter
            self.scores[player] += 1
            return True
        else:
            print(f"Wrong guess! The letter {letter} is not in the word.")
            self.remaining_guesses -= 1
            return False

    def display(self) -> None:
        print("Word: " + " ".join(self.guessed_word))
        print(f"Guesses left: {self.remaining_guesses}")
        print("Scores: " + ", ".join([f"{player}: {score}" for player, score in self.scores.items()]))
        print("Guessed letters: " + ", ".join(sorted(self.guessed_letters)))

    def is_finished(self) -> bool:
        return self.remaining_guesses <= 0 or "_" not in self.guessed_word

    def get_result(self) -> str:
        if "_" not in self.guessed_word:
            return f"You guessed the word! Final Scores: {self.scores}"
        else:
            return f"Out of guesses. The word was '{self.word}'. Final Scores: {self.scores}"

    def next_player(self) -> str:
        self.current_player_index: int = (self.current_player_index + 1) % len(self.players)
        return self.players[self.current_player_index]
