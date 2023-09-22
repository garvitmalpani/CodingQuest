import tkinter as tk
import random
import tkinter.messagebox as messagebox

# Define categories and words
CATEGORIES = {
    "Daily Household Items": ["TELEVISION", "CAR", "WATCH", "AIRCONDITIONER", "REFRIGERATOR", "MICROWAVE",
                              "DISHWASHER", "COFFEE", "VACUUMCLEANER", "WASHINGMACHINE", "BLENDER", "IRON",
                              "TOASTER", "HAIRDRYER", "COMPUTER", "CLOCK", "SOFA", "TABLE", "LAMP", "VACUUM"],

    "Tech Products": ["LAPTOP", "SMARTPHONE", "HEADPHONES", "CAMERA", "KEYBOARD", "MOUSE", "MONITOR", "ROUTER",
                      "SPEAKER", "TABLET", "PRINTER", "PROJECTOR", "MICROPHONE", "DRONE", "WEBCAM", "GPS",
                      "SMARTWATCH", "GAMINGCONSOLE", "FLASHDRIVE", "EARBUDS"],

    "Famous Car Brands": ["TOYOTA", "HONDA", "BMW", "MERCEDES", "FORD", "CHEVROLET", "NISSAN", "VOLKSWAGEN",
                         "AUDI", "LEXUS", "HYUNDAI", "JEEP", "SUBARU", "TESLA", "FIAT", "MAZDA", "ACURA", "KIA",
                         "BUICK", "CADILLAC"],

    "Famous Clothing Brands": ["NIKE", "ADIDAS", "GUCCI", "VERSACE", "PRADA", "LOUISVUITTON", "CHANEL", "RALPHLAUREN",
                             "PUMA", "ROADSTER", "ZARA", "CALVIN KLEIN", "TOMMYHILFIGER", "ARMANI", "FILA", "VANS", "UNDERARMOUR",
                             "REEBOK", "CONVERSE", "LEVIS"],
                             
    "Fruits Name": ["APPLE", "BANANA", "ORANGE", "MANGO", "STRAWBERRY", "BLUEBERRY", "PINEAPPLE", "WATERMELON",
               "GRAPE", "KIWI", "PEACH", "PEAR", "APRICOT", "CHERRY", "LEMON", "LIME", "COCONUT", "AVOCADO",
               "PAPAYA", "PLUM"]
}



class GuessTheWordGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guess The Word")

        # Set the window size and position
        self.root.geometry("800x420")
        self.root.state('zoomed')  # Maximize the window

        # Game description and rules
        self.description_label = tk.Label(root, text="GUESS THE WORD", font=("Helvetica Neue", 24, "bold"))
        self.description_label.pack(pady=(20, 10))

        self.rules_label = tk.Label(root, text="Select a category and guess the word to win. You have limited guesses!", font=("Helvetica Neue", 14))
        self.rules_label.pack()

        # Initialize game variables
        self.category = None
        self.word_to_guess = None
        self.guesses_left = 6
        self.current_word = None
        self.used_letters = set()
        self.wrong_letters = []

        # Create GUI elements
        self.category_label = tk.Label(root, text="Select a Category:", font=("Helvetica Neue", 16))
        self.category_label.pack()

        # Create buttons for category selection
        self.category_buttons_frame = tk.Frame(root)
        self.category_buttons_frame.pack(pady=10)

        self.category_buttons = []
        for category in CATEGORIES.keys():
            button = tk.Button(self.category_buttons_frame, text=category, command=lambda cat=category: self.start_game(cat), font=("Helvetica Neue", 16))
            button.pack(fill=tk.X, padx=20, pady=5)
            self.category_buttons.append(button)

        # Hide game elements initially
        self.hide_game_elements()

    def start_game(self, category):
        self.category = category
        self.hide_category_selection()
        self.initialize_game()

    def hide_category_selection(self):
        self.category_label.pack_forget()
        self.category_buttons_frame.pack_forget()

    def initialize_game(self):
        self.word_to_guess = random.choice(CATEGORIES[self.category])
        self.guesses_left = 6
        self.current_word = ["_"] * len(self.word_to_guess)
        self.used_letters.clear()
        self.wrong_letters.clear()

        self.show_game_elements()

    def show_game_elements(self):
        self.guess_label = tk.Label(self.root, text=f"Guesses left: {self.guesses_left}", font=("Helvetica Neue", 16))
        self.guess_label.pack()

        self.word_label = tk.Label(self.root, text=" ".join(self.current_word), font=("Helvetica Neue", 24))
        self.word_label.pack(pady=10)

        self.letter_entry = tk.Entry(self.root, width=5, font=("Helvetica Neue", 16))
        self.letter_entry.pack()
        self.letter_entry.bind("<Return>", lambda event=None: self.make_guess())

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.guess_button = tk.Button(button_frame, text="Guess", command=self.make_guess, font=("Helvetica Neue", 16))
        self.guess_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_game, font=("Helvetica Neue", 16), state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        self.wrong_letters_label = tk.Label(self.root, text="Wrong Letters: ", font=("Helvetica Neue", 16))
        self.wrong_letters_label.pack()

    def hide_game_elements(self):
        if hasattr(self, 'guess_label'):
            self.guess_label.pack_forget()
            self.word_label.pack_forget()
            self.letter_entry.pack_forget()
            self.guess_button.pack_forget()
            self.reset_button.pack_forget()
            self.wrong_letters_label.pack_forget()

    def make_guess(self):
        guess = self.letter_entry.get().upper()

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showerror("Invalid Input", "Please enter a single letter.")
            self.letter_entry.delete(0, tk.END)
            return

        if guess in self.used_letters:
            messagebox.showerror("Invalid Guess", f"You already guessed '{guess}'. Try a different letter.")
            self.letter_entry.delete(0, tk.END)
            return

        self.letter_entry.delete(0, tk.END)

        self.used_letters.add(guess)

        if guess in self.word_to_guess:
            for i, letter in enumerate(self.word_to_guess):
                if letter == guess:
                    self.current_word[i] = guess
            self.word_label.config(text=" ".join(self.current_word))
        else:
            self.guesses_left -= 1
            self.wrong_letters.append(guess)
            self.wrong_letters_label.config(text="Wrong Letters: " + ", ".join(self.wrong_letters))
            self.guess_label.config(text=f"Guesses left: {self.guesses_left}")

        if self.guesses_left == 0:
            self.word_label.config(text=f"You lose! The word was '{self.word_to_guess}'.", fg="red")
            self.letter_entry.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            messagebox.showinfo("Game Over", f"You lose! The word was '{self.word_to_guess}'.")
        elif "_" not in self.current_word:
            self.word_label.config(text="Congratulations! You guessed the word.", fg="green")
            self.letter_entry.config(state=tk.DISABLED)
            self.reset_button.config(state=tk.NORMAL)
            messagebox.showinfo("Game Over", "Congratulations! You guessed the word.")

    def reset_game(self):
        self.hide_game_elements()
        self.show_category_selection()

    def show_category_selection(self):
        self.category_label.pack()
        self.category_buttons_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = GuessTheWordGame(root)
    root.mainloop()
