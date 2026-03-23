import tkinter as tk
from tkinter import messagebox
import random

class PidginScrabble:
    def __init__(self, root):
        self.root = root
        self.root.title("FRANK'S PIDGIN BUILDER PRO")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")

        # The expanded Pidgin Dictionary (All Caps to match tiles)
        self.dictionary = [
            "CHOP", "SABI", "WAHALA", "KOLO", "JARA", "OYIBO", "WEY", "BASH", "PIKIN",
            "ABI", "BAFFS", "BELLE", "BLESS", "BOKU", "BONANZA", "COMOT", "DASH", "DON",
            "DONE", "FAYA", "FINI", "GBANA", "JOLLY", "KEKE", "KPAKO", "KPAI", "KULI",
            "MAGUN", "MUMU", "NAWA", "OBODO", "OKADA", "PADI", "SHAYO", "TIWA", "UNAH",
            "VAMOOSE", "WETIN", "YAPPA", "ZANGA"
        ]

        self.score, self.lives = 0, 3
        self.current_letters = []

        # UI Elements in Pidgin English
        self.score_label = tk.Label(root, text="POINTS: 0", fg="gold", bg="#1a1a1a", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=20)

        self.lives_label = tk.Label(root, text="❤️❤️❤️", fg="red", bg="#1a1a1a", font=("Arial", 18))
        self.lives_label.pack()

        self.letter_frame = tk.Frame(root, bg="#1a1a1a")
        self.letter_frame.pack(pady=10)

        self.word_entry = tk.Entry(root, font=("Arial", 18), justify='center', bg="#333", fg="white", insertbackground="white")
        self.word_entry.pack(pady=10)
        
        # Allows you to press 'Enter' on your keyboard to submit
        self.word_entry.bind("<Return>", lambda event: self.check_word())

        self.submit_btn = tk.Button(root, text="SUBMIT", command=self.check_word, bg="gold", font=("Arial", 14, "bold"), width=15)
        self.submit_btn.pack(pady=10)

        self.next_round()

    def next_round(self):
        # Clear previous letter tiles
        for widget in self.letter_frame.winfo_children():
            widget.destroy()

        # Pick a word from our Pidgin list and scramble it
        target = random.choice(self.dictionary)
        # Add a few random letters to make it a bit harder
        extra = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2))
        self.current_letters = list(target + extra)
        random.shuffle(self.current_letters)

        # Create the visual letter tiles
        for letter in self.current_letters:
            lbl = tk.Label(self.letter_frame, text=letter, font=("Arial", 20, "bold"),
                          width=2, relief="raised", bg="gold", fg="black")
            lbl.pack(side="left", padx=5)

    def check_word(self):
        user_word = self.word_entry.get().upper().strip()
        self.word_entry.delete(0, tk.END)

        if user_word in self.dictionary:
            # Logic check: Did the user actually use the letters provided?
            temp_letters = self.current_letters.copy()
            can_form = True
            for char in user_word:
                if char in temp_letters:
                    temp_letters.remove(char)
                else:
                    can_form = False
                    break
            
            if can_form:
                self.score += 10
                self.score_label.config(text=f"POINTS: {self.score}")
                self.next_round()
            else:
                self.wrong_answer("No use the wrong letters!")
        else:
            self.wrong_answer("Oga, that no be word!")

    def wrong_answer(self, reason):
        self.lives -= 1
        self.lives_label.config(text="❤️" * self.lives)
        if self.lives <= 0:
            self.end_game()
        else:
            messagebox.showwarning("E No Correct", reason)

    def end_game(self):
        messagebox.showinfo("Game Finish!", f"Final Score: {self.score}\nOga, you try!")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = PidginScrabble(root)
    root.mainloop()