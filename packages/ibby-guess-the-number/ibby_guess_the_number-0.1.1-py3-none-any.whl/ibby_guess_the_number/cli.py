"""Command-line interface for ibby-guess-the-number."""

from .game import guess_the_number

def main() -> None:
    """Entry point for the ibby-guess-the-number CLI."""
    guess_the_number()

if __name__ == "__main__":
    main() 