# UltimateNumberGUI.py

import tkinter as tk
from tkinter import messagebox
from Background import GameLogic
import tkinter.font as tkFont

class UltimateNumberGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ultimate Number Game")
        master.geometry("400x380") # Adjust height slightly as one row of buttons is removed
        master.option_add('*Font', 'Arial 12')

        self.game_logic = GameLogic()

        # Frame for range selection page
        self.range_frame = tk.Frame(master)

        self.range_label = tk.Label(self.range_frame, text="Choose a number range:", font=('Arial', 14, 'bold'))
        self.range_label.grid(row=0, column=0, columnspan=2, pady=15)

        # === Adjusted button layout after removing 1000 ===
        self.btn_range_20 = tk.Button(self.range_frame, text="0 - 20", width=10, command=lambda: self.start_game(20))
        self.btn_range_20.grid(row=1, column=0, padx=10, pady=5)

        self.btn_range_30 = tk.Button(self.range_frame, text="0 - 30", width=10, command=lambda: self.start_game(30))
        self.btn_range_30.grid(row=1, column=1, padx=10, pady=5)

        self.btn_range_50 = tk.Button(self.range_frame, text="0 - 50", width=10, command=lambda: self.start_game(50))
        self.btn_range_50.grid(row=2, column=0, padx=10, pady=5)

        self.btn_range_100 = tk.Button(self.range_frame, text="0 - 100", width=10, command=lambda: self.start_game(100))
        self.btn_range_100.grid(row=2, column=1, padx=10, pady=5)

        self.btn_range_200 = tk.Button(self.range_frame, text="0 - 200", width=10, command=lambda: self.start_game(200))
        self.btn_range_200.grid(row=3, column=0, padx=10, pady=5)

        self.btn_range_500 = tk.Button(self.range_frame, text="0 - 500", width=10, command=lambda: self.start_game(500))
        self.btn_range_500.grid(row=3, column=1, padx=10, pady=5)

        # === Removed btn_range_1000 ===


        # === Centering Configuration for range_frame ===
        self.range_frame.grid_columnconfigure(0, weight=1)
        self.range_frame.grid_columnconfigure(1, weight=1)
        self.range_frame.grid_rowconfigure(0, weight=1) # Weight above label
        self.range_frame.grid_rowconfigure(4, weight=1) # Adjusted weight below buttons (now row 4 is below row 3)


        # Frame for game play page (initially hidden)
        self.game_frame = tk.Frame(master)

        # Current Range Label (Large and Bold)
        self.current_range_label = tk.Label(self.game_frame, text="", font=('Arial', 24, 'bold'))
        self.current_range_label.grid(row=1, column=0, columnspan=2, pady=10) # Row 1

        self.guess_entry = tk.Entry(self.game_frame, width=10, font=('Arial', 14))
        self.guess_entry.grid(row=3, column=0, padx=5, pady=10, sticky='e') # Row 3
        self.guess_entry.bind("<Return>", lambda event=None: self.make_guess())

        self.submit_button = tk.Button(self.game_frame, text="Guess", command=self.make_guess)
        self.submit_button.grid(row=3, column=1, padx=5, pady=10, sticky='w') # Row 3

        # Guesses Remaining Label (Below Input)
        self.guesses_label = tk.Label(self.game_frame, text="")
        self.guesses_label.grid(row=4, column=0, columnspan=2, pady=5) # Row 4

        # Feedback Label
        self.feedback_label = tk.Label(self.game_frame, text="", wraplength=350, justify='center')
        self.feedback_label.grid(row=5, column=0, columnspan=2, pady=10) # Row 5

        # Show Answer Button (Always visible during game play)
        self.show_answer_button = tk.Button(self.game_frame, text="Show Answer", command=self.show_answer)
        self.show_answer_button.grid(row=6, column=0, columnspan=2, pady=10) # Placed in Row 6, centered

        # Play Again Button (Only visible after game ends)
        self.play_again_button = tk.Button(self.game_frame, text="Play Again?", command=self.reset_game)
        # Will be gridded in end_game, placed in row 7


        # === Centering Configuration for game_frame ===
        self.game_frame.grid_columnconfigure(0, weight=1)
        self.game_frame.grid_columnconfigure(1, weight=1)
        self.game_frame.grid_rowconfigure(0, weight=1) # Weight above the range label
        self.game_frame.grid_rowconfigure(8, weight=1) # Weight below all elements (up to row 7)


        # --- Initial View Setup ---
        self.range_frame.grid(row=0, column=0, sticky="nsew") # Show range selection initially

        # === Centering Configuration for the master window ===
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)


    # --- GUI Control and Interaction Methods (No changes needed here) ---

    def start_game(self, selected_upper_bound):
        """Initializes game logic and switches to game view."""
        try:
            self.game_logic.start_new_game(selected_upper_bound)

            self.range_frame.grid_forget()
            self.game_frame.grid(row=0, column=0, sticky="nsew")

            self.update_display()
            self.feedback_label.config(text=f"I'm thinking of a number between 0 and {self.game_logic.get_upper_bound()}. Enter your first guess!")

            self.guess_entry.config(state='normal')
            self.submit_button.config(state='normal')

            self.play_again_button.grid_forget() # Hide Play Again button

            self.guess_entry.focus_set()

        except ValueError as e:
            messagebox.showerror("Error", str(e))


    def make_guess(self):
        """Gets guess from GUI, sends to logic, updates GUI based on result."""
        guess_str = self.guess_entry.get().strip()
        self.guess_entry.delete(0, tk.END)

        if not guess_str:
            self.feedback_label.config(text="Please enter a number.")
            self.guess_entry.focus_set()
            return

        try:
            user_guess = int(guess_str)
            if not (0 <= user_guess <= self.game_logic.get_upper_bound()):
                 self.feedback_label.config(text=f"Your guess ({user_guess}) is outside the original range (0 - {self.game_logic.get_upper_bound()}).")
                 self.guess_entry.focus_set()
                 return

        except ValueError:
            self.feedback_label.config(text="Invalid input. Please enter an integer number.")
            self.guess_entry.focus_set()
            return

        result = self.game_logic.process_guess(user_guess)

        if result == 'win':
            secret = self.game_logic.get_secret_number()
            guesses = self.game_logic.get_guess_limit() - self.game_logic.get_guesses_remaining()
            self.end_game(f"Congratulations! You guessed the number {secret} in {guesses} guesses.")
        elif result == 'super_win':
             secret = self.game_logic.get_secret_number()
             self.end_game(f"SUPER WIN!!!! The number is {secret}!")
        elif result == 'too_low':
            self.feedback_label.config(text="Too low!")
            self.update_display()
        elif result == 'too_high':
            self.feedback_label.config(text="Too high!")
            self.update_display()
        elif result == 'lost':
            secret = self.game_logic.get_secret_number()
            self.end_game(f"Sorry, you ran out of guesses. The number was {secret}.")

        if not self.game_logic.is_game_over():
             self.guess_entry.focus_set()


    def update_display(self):
        min_val, max_val = self.game_logic.get_current_range()
        self.current_range_label.config(text=f"{min_val} - {max_val}")
        self.guesses_label.config(text=f"Guesses remaining: {self.game_logic.get_guesses_remaining()}")

    def end_game(self, message):
        self.feedback_label.config(text=message)
        self.guess_entry.config(state='disabled')
        self.submit_button.config(state='disabled')

        # Show Play Again button
        self.play_again_button.grid(row=7, column=0, columnspan=2, pady=10) # Adjusted row


    def show_answer(self):
        secret = self.game_logic.get_secret_number()

        if not self.game_logic.is_game_over():
            self.end_game(f"You gave up! The number was {secret}.")
        else:
            messagebox.showinfo("Secret Number", f"The secret number was: {secret}")


    def reset_game(self):
        self.game_frame.grid_forget()
        self.range_frame.grid(row=0, column=0, sticky="nsew")

        self.feedback_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.play_again_button.grid_forget() # Hide Play Again button


# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    game_gui = UltimateNumberGUI(root)
    root.mainloop()