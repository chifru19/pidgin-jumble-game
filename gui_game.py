import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") 

# A list of valid Pidgin words the game recognizes
VALID_PIDGIN_WORDS = [
    "pikin", "sabi", "motto", "boku", "kakaki", "overtake", 
    "wakabout", "bellefull", "confam", "expensiv", "ogbonge", 
    "kpatakpata", "oya", "chop", "muna", "una", "shayo"
]

class PidginScrabbleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Frank's Pidgin Builder")
        self.geometry("400x700")

        self.level_names = ["Pikin", "Agbero", "Ogbonge"]
        
        # UI Setup
        self.label_title = ctk.CTkLabel(self, text="🎮 PIDGIN BUILDER", font=("Arial", 28, "bold"))
        self.label_title.pack(pady=(30, 5))

        self.label_timer = ctk.CTkLabel(self, text="Time: 20s", font=("Arial", 20), text_color="#FF5555")
        self.label_timer.pack()

        self.label_rank = ctk.CTkLabel(self, text="", text_color="#00FF00", font=("Arial", 16))
        self.label_rank.pack()

        self.label_stats = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.label_stats.pack(pady=10)

        # The "Letter Rack"
        self.label_rack_title = ctk.CTkLabel(self, text="YOUR LETTERS:", font=("Arial", 12))
        self.label_rack_title.pack(pady=(20, 0))
        
        self.label_letters = ctk.CTkLabel(self, text="", font=("Courier New", 44, "bold"), text_color="#FFCC00")
        self.label_letters.pack(pady=20)

        self.entry_word = ctk.CTkEntry(self, placeholder_text="Build a word...", width=280, height=50, font=("Arial", 20))
        self.entry_word.pack(pady=10)

        self.btn_check = ctk.CTkButton(self, text="SUBMIT WORD", command=self.check_word, font=("Arial", 16, "bold"), height=40)
        self.btn_check.pack(pady=20)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=10)

        self.btn_restart = ctk.CTkButton(self, text="PLAY AGAIN", command=self.reset_game_state, fg_color="orange", text_color="black")
        
        self.reset_game_state()

    def reset_game_state(self):
        self.score = 0
        self.lives = 3
        self.current_rank_idx = 0
        self.btn_restart.pack_forget()
        self.btn_check.configure(state="normal")
        self.entry_word.configure(state="normal")
        self.update_ui()
        self.next_round()

    def generate_hand(self):
        vowels = "AEIOU"
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
        # Always give at least 3 vowels and 4 consonants for fairness
        hand = [random.choice(vowels) for _ in range(3)] + [random.choice(consonants) for _ in range(4)]
        random.shuffle(hand)
        return hand

    def next_round(self):
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        
        self.time_left = 20
        self.current_hand = self.generate_hand()
        self.label_letters.configure(text=" ".join(self.current_hand))
        self.entry_word.delete(0, 'end')
        self.start_timer()

    def start_timer(self):
        if self.lives > 0:
            if self.time_left > 0:
                self.time_left -= 1
                self.label_timer.configure(text=f"Time: {self.time_left}s")
                self.timer_id = self.after(1000, self.start_timer)
            else:
                self.lives -= 1
                self.label_feedback.configure(text="⏰ Time Up! Lose 1 Life.", text_color="red")
                if self.lives > 0: self.next_round()
                else: self.end_game()
                self.update_ui()

    def check_word(self):
        user_word = self.entry_word.get().lower().strip()
        
        # 1. Check if word is in our dictionary
        if user_word not in VALID_PIDGIN_WORDS:
            self.label_feedback.configure(text=f"'{user_word}' is not a Pidgin word!", text_color="orange")
            return

        # 2. Check if letters are available in the hand
        temp_hand = [letter.lower() for letter in self.current_hand]
        can_build = True
        for char in user_word:
            if char in temp_hand:
                temp_hand.remove(char)
            else:
                can_build = False
                break
        
        if can_build:
            points = len(user_word) * 5
            self.score += points
            self.label_feedback.configure(text=f"Correct! +{points} points", text_color="#00FF00")
            
            # Rank Up Logic
            if self.score > 50: self.current_rank_idx = 1
            if self.score > 150: self.current_rank_idx = 2
            
            self.next_round()
        else:
            self.label_feedback.configure(text="You don't have those letters!", text_color="red")
        
        self.update_ui()

    def update_ui(self):
        self.label_rank.configure(text=f"RANK: {self.level_names[self.current_rank_idx]}")
        self.label_stats.configure(text=f"Score: {self.score}  |  Lives: