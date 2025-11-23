from utils import *

print_instructions()
while True:
    aborted_or_won = play_round()
    # If the player typed 'quit' during play_round, we returned False (treated as abort).
    # We still ask whether to play again for clarity.
    if not ask_play_again():
        print("Thanks for playing — goodbye!")
        break
    print("\nStarting a new game...\n" + ("-" * 50) + "\n")