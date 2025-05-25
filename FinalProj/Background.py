# Background.py

import random

class GameLogic:
    """
    Contains the core logic for the Ultimate Number game.
    Does not handle any user interface.
    """
    def __init__(self):
        self._secret_number = None
        self._upper_bound = None
        self._guess_limit = None
        self._guesses_taken = 0
        self._min_range = 0 # Internal tracking of the guessed range
        self._max_range = 0 # Internal tracking of the guessed range
        self._is_game_over = False

        # Define range options and corresponding guess limits
        # (upper_bound, guess_limit) for range 0 to upper_bound
        # Removed 1000 range
        self._range_options = {
            20: 6,
            30: 7,
            50: 8,
            100: 10,
            200: 12,
            500: 15
        }

    def start_new_game(self, selected_upper_bound):
        """Initializes game state for a new game."""
        if selected_upper_bound not in self._range_options:
            raise ValueError(f"Invalid upper bound: {selected_upper_bound}. Must be one of {list(self._range_options.keys())}")

        self._upper_bound = selected_upper_bound
        self._guess_limit = self._range_options[self._upper_bound]
        self._secret_number = random.randint(0, self._upper_bound)
        self._min_range = 0
        self._max_range = self._upper_bound
        self._guesses_taken = 0
        self._is_game_over = False

        # print(f"DEBUG: Secret number is {self._secret_number}") # Optional: for debugging

    def process_guess(self, user_guess):
        """
        Processes a user's guess and updates game state.
        Returns a string indicating the result:
        'win', 'super_win', 'too_low', 'too_high', 'lost', 'invalid_guess'
        """
        if self._is_game_over:
            return 'game_over'

        if not isinstance(user_guess, int):
             return 'invalid_guess'

        self._guesses_taken += 1

        if user_guess == self._secret_number:
            if self._max_range - self._min_range == 2:
                self._is_game_over = True
                return 'super_win'
            else:
                self._is_game_over = True
                return 'win'
        elif user_guess < self._secret_number:
            self._min_range = max(self._min_range, user_guess)
            result = 'too_low'
        else: # user_guess > self._secret_number
            self._max_range = min(self._max_range, user_guess)
            result = 'too_high'

        if self._guesses_taken >= self._guess_limit and not self._is_game_over:
            self._is_game_over = True
            result = 'lost'

        return result

    def get_current_range(self):
        return (self._min_range, self._max_range)

    def get_guesses_remaining(self):
        return self._guess_limit - self._guesses_taken

    def get_secret_number(self):
        return self._secret_number

    def get_upper_bound(self):
        return self._upper_bound

    def is_game_over(self):
        return self._is_game_over

    def get_guess_limit(self):
        return self._guess_limit