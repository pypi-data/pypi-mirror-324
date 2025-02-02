import random
from enum import Enum, auto

MIN_NUMBER = 1
MAX_NUMBER = 100

class GameState(Enum):
    TOO_LOW = auto()
    TOO_HIGH = auto()
    WIN = auto()
    
    def get_message(self, attempts: int = None) -> str:
        messages = {
            GameState.TOO_LOW: "Your guess is too low.",
            GameState.TOO_HIGH: "Your guess is too high.",
            GameState.WIN: f"Congratulations! You guessed the number in {attempts} attempts."
        }
        return messages[self]

def validate_guess(guess: str) -> int:
    try:
        return int(guess)
    except ValueError:
        raise ValueError("Please enter a valid number.")

def get_user_guess() -> int:
    while True:
        guess = input("Take a guess: ")
        try:
            return validate_guess(guess)
        except ValueError as e:
            print(e)

def guess_the_number() -> None:
    number_to_guess = random.randint(MIN_NUMBER, MAX_NUMBER)
    attempts = 0
    
    print(f"Welcome to 'Guess the Number'!\nI'm thinking of a number between {MIN_NUMBER} and {MAX_NUMBER}.")

    while True:
        guess = get_user_guess()
        attempts += 1

        if guess < MIN_NUMBER or guess > MAX_NUMBER:
            print(f"Please enter a number between {MIN_NUMBER} and {MAX_NUMBER}.")
            continue

        if guess < number_to_guess:
            state = GameState.TOO_LOW
        elif guess > number_to_guess:
            state = GameState.TOO_HIGH
        else:
            state = GameState.WIN
            
        print(state.get_message(attempts if state == GameState.WIN else None))
        
        if state == GameState.WIN:
            break

if __name__ == "__main__":
    guess_the_number()