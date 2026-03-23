import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green") 

class PidginJumbleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Frank's Pidgin Jumble")
        self.geometry("360x640")

        self.levels = {
            "Pikin": ["pikin", "sabi", "motto", "boku"],
            "Agbero": ["kakaki", "overtake", "wakabout", "bellefull"],
            "Ogbonge": ["confam", "expensiv", "ogbonge", "kpatakpata"]
        }
        self.level_names = list(self.levels.keys())
        
        # UI Setup
        self.label_title = ctk.CTkLabel(self, text="🎮 FRANK'S JUMBLE", font=("Arial", 26, "bold"))
        self.label_title.pack(pady=(30, 5))

        self.label_timer = ctk.CTkLabel(self, text="Time: 15s", font=("Arial", 20), text_color="#FF5555")
        self.label_timer.pack()

        self.label_level = ctk.CTkLabel(self, text="", text_color="#00FF00")
        self.label_level.pack()

        self.label_stats = ctk.CTkLabel(self, text="", font=("Arial", 18))
        self.label_stats.pack(pady=10)

        self.label_jumbled = ctk.CTkLabel(self, text="", font=("Arial", 40, "bold"), text_color="#FFCC00")
        self.label_jumbled.pack(pady=40)

        self.entry_guess = ctk.CTkEntry(self, placeholder_text="Type word here...", width=250, height=45)
        self.entry_guess.pack(pady=10)

        self.btn_check = ctk.CTkButton(self, text="SUBMIT", command=self.check_answer, font=("Arial", 16, "bold"))
        self.btn_check.pack(pady=20)

        self.label_feedback = ctk.CTkLabel(self, text="", font=("Arial", 14))
        self.label_feedback.pack(pady=10)

        self.btn_restart = ctk.CTkButton(self, text="PLAY AGAIN", command=self.reset_game_state, fg_color="orange", text_color="black")
        
        self.reset_game_state()

    def reset_game_state(self):
        self.current_level_idx = 0
        self.score = 0
        self.lives = 3
        self.time_left = 15
        self.btn_restart.pack_forget()
        self.btn_check.configure(state="normal")
        self.entry_guess.configure(state="normal")
        self.update_ui()
        self.next_round()

    def start_timer(self):
        if self.lives > 0:
            if self.time_left > 0:
                self.time_left -= 1
                self.label_timer.configure(text=f"Time: {self.time_left}s")
                self.timer_id = self.after(1000, self.start_timer)
            else:
                self.lives -= 1
                self.label_feedback.configure(text="⏰ Time Up! Lose 1 Life.", text_color="red")
                if self.lives > 0:
                    self.next_round()
                else:
                    self.end_game()
                self.update_ui()

    def update_ui(self):
        self.label_level.configure(text=f"RANK: {self.level_names[self.current_level_idx]}")
        self.label_stats.configure(text=f"Score: {self.score}  |  Lives: {'❤️' * self.lives}")

    def next_round(self):
        # Cancel any existing timer before starting a new one
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        
        self.time_left = 15
        self.label_timer.configure(text="Time: 15s")
        
        current_rank = self.level_names[self.current_level_idx]
        self.target_word = random.choice(self.levels[current_rank])
        jumbled = list(self.target_word)
        random.shuffle(jumbled)
        self.label_jumbled.configure(text="".join(jumbled).upper())
        self.entry_guess.delete(0, 'end')
        self.start_timer()

    def check_answer(self):
        guess = self.entry_guess.get().lower().strip()
        if guess == self.target_word:
            self.score += 10
            if self.score >= 30 and self.current_level_idx < len(self.level_names) - 1:
                self.current_level_idx += 1
            self.next_round()
        else:
            self.lives -= 1
            if self.lives <= 0:
                self.end_game()
            else:
                self.next_round()
        self.update_ui()

    def end_game(self):
        if hasattr(self, 'timer_id'):
            self.after_cancel(self.timer_id)
        self.label_jumbled.configure(text="GAME OVER", text_color="red")
        self.btn_check.configure(state="disabled")
        self.entry_guess.configure(state="disabled")
        self.btn_restart.pack(pady=10)

if __name__ == "__main__":
    app = PidginJumbleApp()
    app.mainloop()