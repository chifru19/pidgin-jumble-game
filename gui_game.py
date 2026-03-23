import tkinter as tk
from tkinter import messagebox
import random

class PidginScrabble:
    def __init__(self, root):
        self.root = root
        self.root.title("FRANK'S PIDGIN BUILDER PRO")
        self.root.geometry("500x750")
        self.root.configure(bg="#1a1a1a")

        self.dictionary = [
            "CHOP", "SABI", "WAHALA", "KOLO", "JARA", "OYIBO", "WEY", "BASH", "PIKIN",
            "ABI", "BAFFS", "BELLE", "BLESS", "BOKU", "BONANZA", "COMOT", "DASH", "DON",
            "DONE", "FAYA", "FINI", "GBANA", "JOLLY", "KEKE", "KPAKO", "KPAI", "KULI",
            "MAGUN", "MUMU", "NAWA", "OBODO", "OKADA", "PADI", "SHAYO", "TIWA", "UNAH",
            "VAMOOSE", "WETIN", "YAPPA", "ZANGA"
        ]

        self.score, self.lives = 0, 3
        self.current_letters = []
        self.target_word = "" 

        # UI Elements
        self.score_label = tk.Label(root, text="POINTS: 0", fg="gold", bg="#1a1a1a", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=20)

        self.lives_label = tk.Label(root, text="❤️❤️❤️", fg="red", bg="#1a1a1a", font=("Arial", 18))
        self.lives_label.pack()

        self.letter_frame = tk.Frame(root, bg="#1a1a1a")
        self.letter_frame.pack(pady=20)

        self.word_entry = tk.Entry(root, font=("Arial", 18), justify='center', bg="#333", fg="white", insertbackground="white")
        self.word_entry.pack(pady=10)
        self.word_entry.focus_set() 
        self.word_entry.bind("<Return>", lambda event: self.check_word())

        self.submit_btn = tk.Button(root, text="SUBMIT", command=self.check_word, bg="gold", font=("Arial", 14, "bold"), width=15)
        self.submit_btn.pack(pady=10)

        self.hint_btn = tk.Button(root, text="GET HINT (-5 PTS)", command=self.give_hint, bg="#444", fg="white", font=("Arial", 10), width=15)
        self.hint_btn.pack(pady=5)

        self.next_round()

    def next_round(self):
        for widget in self.letter_frame.winfo_children():
            widget.destroy()

        self.target_word = random.choice(self.dictionary) 
        
        # Ensures enough letters for double-letter words like KOLO or BELLE
        word_letters = list(self.target_word)
        extra = random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3)
        
        self.current_letters = word_letters + extra
        random.shuffle(self.current_letters)

        for letter in self.current_letters:
            lbl = tk.Label(self.letter_frame, text=letter, font=("Arial", 20, "bold"),
                          width=2, relief="raised", bg="gold", fg="black")
            lbl.pack(side="left", padx=5)

    def give_hint(self):
        if self.score >= 5:
            self.score -= 5
            self.score_label.config(text=f"POINTS: {self.score}")
            messagebox.showinfo("Hint", f"The word starts with: {self.target_word[0]}")
        else:
            messagebox.showwarning("No Points", "Oga, you no get enough points for hint!")

    def check_word(self):
        user_word = self.word_entry.get().upper().strip()
        self.word_entry.delete(0, tk.END)

        if user_word in self.dictionary:
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
                self.wrong_answer()
        else:
            self.wrong_answer()

    def wrong_answer(self):
        self.lives -= 1
        self.lives_label.config(text="❤️" * self.lives)
        if self.lives <= 0:
            messagebox.showinfo("Game Over", f"Final Score: {self.score}")
            self.score = 0
            self.lives = 3
            self.score_label.config(text="POINTS: 0")
            self.lives_label.config(text="❤️❤️❤️")
        else:
            messagebox.showerror("Wrong", "Try again!")

# THE ENGINE: These lines must have NO spaces at the beginning
if __name__ == "__main__":
    root = tk.Tk()
    game = PidginScrabble(root)
    root.mainloop()