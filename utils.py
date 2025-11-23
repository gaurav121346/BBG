import random

def generate_secret():
    """Return a 3-digit secret string (no repeated digits, no leading zero)."""
    digits = list("0123456789")
    while True:
        # choose a first digit from 1-9 to avoid leading zero
        first = random.choice(digits[1:])
        remaining = digits.copy()
        remaining.remove(first)
        # pick two distinct remaining digits
        a, b = random.sample(remaining, 2)
        secret = first + a + b
        # defensive: ensure no repeats (we sampled distinct) and length 3
        if len(secret) == 3 and len(set(secret)) == 3:
            return secret

def validate_guess(guess):
    """
    Validate guess string. Returns (ok: bool, message: str).
    Requirements:
      - exactly 3 characters
      - all digits
      - no leading zero
      - no repeated digits
    """
    if not guess:
        return False, "Empty input."
    if not guess.isdigit():
        return False, "Guess must contain only digits (0-9)."
    if len(guess) != 3:
        return False, "Guess must be exactly 3 digits long."
    if guess[0] == '0':
        return False, "Leading zero not allowed; guess must be between 100 and 999."
    if len(set(guess)) != 3:
        return False, "Digits must not repeat. Example of invalid guess: 554."
    return True, ""

def score_guess(secret, guess):
    """
    Return (bulls, bears, goats) for given secret and guess.
    Assumes secret and guess are 3-character digit strings with unique digits.
    """
    bulls = sum(1 for s, g in zip(secret, guess) if s == g)
    # For bears: count digits in guess that are in secret but not bulls.
    # Because digits are unique, we can do a simple check.
    bears = sum(1 for g_idx, g in enumerate(guess) if g in secret and secret[g_idx] != g)
    goats = 3 - bulls - bears
    return bulls, bears, goats

def print_instructions():
    print("Welcome to Bulls / Bears / Goats!\n")
    print("Rules:")
    print("- The computer chooses a random 3-digit number (100–999) with no repeated digits.")
    print("- You have 5 guesses to find the secret number.")
    print("- After each guess you'll see counts for:")
    print("    Bulls  = correct digit in the correct position")
    print("    Bears  = correct digit in the wrong position")
    print("    Goats  = digit not in the secret number")
    print()
    print("Example: secret = 549, guess = 592  -->  1 Bull (5), 1 Bear (9), 1 Goat (2)")
    print()
    print("Enter guesses like 549 (no spaces). Leading zero not allowed. Digits must not repeat.")
    print("-" * 50)
    print()

def play_round():
    secret = generate_secret()
    attempts_allowed = 6
    history = []  # list of tuples: (attempt_number, guess, (bulls,bears,goats))

    for attempt in range(1, attempts_allowed + 1):
        # show history
        if history:
            print("\nPrevious guesses:")
            for at, g, (bll, br, gt) in history:
                print(f"  {at:>2}. {g}  ->  Bulls: {bll}  Bears: {br}  Goats: {gt}")
            print()

        # prompt
        raw = input(f"Attempt {attempt}/{attempts_allowed} — Enter your 3-digit guess: ").strip()
        ok, msg = validate_guess(raw)
        if not ok:
            print("Invalid guess:", msg)
            # do not consume attempt on invalid input; give chance again
            # Continue the same attempt number
            # But for robustness, allow player to cancel by entering 'quit' or 'exit'
            if raw.lower() in ('quit', 'exit'):
                print("Exiting current game.")
                return False  # indicates player aborted early
            continue

        guess = raw
        bulls, bears, goats = score_guess(secret, guess)
        history.append((attempt, guess, (bulls, bears, goats)))

        print(f"Result — Bulls: {bulls}, Bears: {bears}, Goats: {goats}")

        if bulls == 3:
            print("\n🎉 Congratulations! You guessed the secret:", secret)
            return True  # player won

    # ran out of attempts
    print("\nYou've used all attempts. The secret number was:", secret)
    return False  # player lost

def ask_play_again():
    while True:
        ans = input("Play again? (y/n): ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        if ans in ('n', 'no'):
            return False
        print("Please answer 'y' or 'n'.")