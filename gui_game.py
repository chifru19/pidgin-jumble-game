import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import os

class PidginScrabble:
    def __init__(self, root, player_name):
        self.root = root
        self.player_name = player_name
        self.root.title(f"FRANK'S PIDGIN BUILDER PRO - {self.player_name}")
        self.root.geometry("500x850")
        self.root.configure(bg="#1a1a1a")
        
        # Ensures window stays in front on Mac
        self.root.attributes('-topmost', True)

        self.dictionary = [
            "CHOP", "SABI", "WAHALA", "KOLO", "JARA", "OYIBO", "WEY", "BASH", "PIKIN",
            "ABI", "BAFFS", "BELLE", "BLESS", "BOKU", "BONANZA", "COMOT", "DASH", "DON",
            "DONE", "FAYA", "FINI", "GBANA", "JOLLY", "KEKE", "KPAKO", "KPAI", "KULI",
            "MAGUN", "MUMU", "NAWA", "OBODO", "OKADA", "PADI", "SHAYO", "TIWA", "UNAH",
            "VAMOOSE", "WETIN", "YAPPA", "ZANGA"
        ]

        self.score, self.lives = 0, 3
        self.target_word = ""
        self.current_letters = []

        # --- UI Elements ---
        self.score_label = tk.Label(root, text="POINTS: 0", fg="gold", bg="#1a1a1a", font=("Arial", 28, "bold"))
        self.score_label.pack(pady=20)

        self.lives_label = tk.Label(root, text="❤️❤️❤️", fg="red", bg="#1a1a1a", font=("Arial", 20))
        self.lives_label.pack()

        # PIDGIN WORD COUNT LABEL
        self.info_label = tk.Label(root, text="", fg="white", bg="#1a1a1a", font=("Arial", 14, "bold"))
        self.info_label.pack(pady=10)

        # HINT DISPLAY
        self.hint_display = tk.Label(root, text="", fg="#00FF00", bg="#1a1a1a", font=("Arial", 14, "italic"))
        self.hint_display.pack(pady=5)

        self.letter_frame = tk.Frame(root, bg="#1a1a1a")
        self.letter_frame.pack(pady=30, fill="x")

        self.word_entry = tk.Entry(root, font=("Arial", 22), justify='center', bg="#333", fg="white", 
                                  insertbackground="white", borderwidth=0, highlightthickness=1)
        self.word_entry.pack(pady=15, ipady=10, padx=50)
        self.word_entry.focus_set()
        self.word_entry.bind("<Return>", lambda event: self.check_word())

        # PIDGIN BUTTONS
        self.submit_btn = tk.Button(root, text="CHOP AM (SUBMIT)", command=self.check_word, bg="#28a745", 
                                   fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.submit_btn.pack(pady=5)

        self.shuffle_btn = tk.Button(root, text="SHUFFLE TILES", command=self.shuffle_tiles, bg="#0056b3", 
                                    fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.shuffle_btn.pack(pady=5)

        self.hint_btn = tk.Button(root, text="HELP ME SMALL (-5 PTS)", command=self.give_hint, bg="#555", 
                                 fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.hint_btn.pack(pady=5)

        self.high_score_label = tk.Label(root, text=self.get_leaderboard_text(), fg="cyan", bg="#1a1a1a", font=("Arial", 11, "italic"))
        self.high_score_label.pack(side="bottom", pady=30)

        self.next_round()

    def next_round(self):
        self.target_word = random.choice(self.dictionary)
        self.hint_display.config(text="") 
        
        # Updated Instruction
        self.info_label.config(text=f"DIS WORD GET {len(self.target_word)} LETTERS")
        
        display_letters = list(self.target_word)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for _ in range(2):
            display_letters.append(random.choice(alphabet))
        
        random.shuffle(display_letters)
        self.current_letters = display_letters
        self.refresh_tiles()
        self.update_ui()

    def refresh_tiles(self):
        for widget in self.letter_frame.winfo_children():
            widget.destroy()
        inner_container = tk.Frame(self.letter_frame, bg="#1a1a1a")
        inner_container.pack(expand=True)
        for letter in self.current_letters:
            lbl = tk.Label(inner_container, text=letter, font=("Arial", 22, "bold"),
                          width=2, height=1, relief="raised", bg="gold", fg="black")
            lbl.pack(side="left", padx=4)

    def shuffle_tiles(self):
        random.shuffle(self.current_letters)
        self.refresh_tiles()

    def give_hint(self):
        if self.score >= 5:
            self.score -= 5
            self.update_ui()
            hint_text = f"E START WITH: {self.target_word[0]}"
            self.hint_display.config(text=hint_text)
            messagebox.showinfo("💡 Hint", f"Look screen! E start with {self.target_word[0]}")
        else:
            messagebox.showwarning("No Cash", "You need 5 points to get help!")

    def check_word(self):
        user_word = self.word_entry.get().upper().strip()
        self.word_entry.delete(0, tk.END)
        if user_word == self.target_word:
            self.score += 10
            self.update_ui()
            messagebox.showinfo("✅ Correct", "Correct! You be pro!")
            self.next_round()
        else:
            self.wrong_answer()

    def update_ui(self):
        self.score_label.config(text=f"POINTS: {self.score}")
        if self.score >= 5:
            self.hint_btn.config(bg="#f1c40f", fg="black")
        else:
            self.hint_btn.config(bg="#555", fg="white")

    def wrong_answer(self):
        self.lives -= 1
        self.lives_label.config(text="❤️" * self.lives)
        self.root.configure(bg="#660000")
        self.root.after(150, lambda: self.root.configure(bg="#1a1a1a"))
        
        if self.lives <= 0:
            # PIDGIN GAME OVER
            messagebox.showinfo("Game Over", f"E DON FINISH! De word na: {self.target_word}")
            self.update_leaderboard()
            self.score, self.lives = 0, 3
            self.lives_label.config(text="❤️❤️❤️")
            self.update_ui()
            self.next_round()
        else:
            messagebox.showerror("Wrong", "No be that one o! Try again!")

    def get_leaderboard_text(self):
        if os.path.exists("leaderboard.txt"):
            try:
                with open("leaderboard.txt", "r") as f:
                    return f"TOP SCORE: {f.read().strip()}"
            except: pass
        return "NO HIGH SCORE YET"

    def update_leaderboard(self):
        current_top = 0
        if os.path.exists("leaderboard.txt"):
            try:
                with open("leaderboard.txt", "r") as f:
                    data = f.read().split(" by ")
                    current_top = int(data[0])
            except: pass
        if self.score > current_top:
            with open("leaderboard.txt", "w") as f:
                f.write(f"{self.score} by {self.player_name}")
            messagebox.showinfo("🏆 Record!", f"New High Score: {self.score}!")
        self.high_score_label.config(text=self.get_leaderboard_text())

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Login", "Who go play?")
    player = name if name and name.strip() else "Guest"
    root.deiconify()
    game = PidginScrabble(root, player)
    root.mainloop()