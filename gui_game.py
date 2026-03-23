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

        # UI Elements
        self.score_label = tk.Label(root, text="POINTS: 0", fg="gold", bg="#1a1a1a", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=10)

        self.lives_label = tk.Label(root, text="❤️❤️❤️", fg="red", bg="#1a1a1a", font=("Arial", 18))
        self.lives_label.pack()

        self.info_label = tk.Label(root, text="Loading...", fg="white", bg="#1a1a1a", font=("Arial", 14))
        self.info_label.pack(pady=5)

        self.letter_frame = tk.Frame(root, bg="#1a1a1a")
        self.letter_frame.pack(pady=20)

        self.word_entry = tk.Entry(root, font=("Arial", 18), justify='center', bg="#333", fg="white", insertbackground="white")
        self.word_entry.pack(pady=10)
        self.word_entry.focus_set()
        self.word_entry.bind("<Return>", lambda event: self.check_word())

        self.submit_btn = tk.Button(root, text="SUBMIT WORD", command=self.check_word, bg="white", fg="black", font=("Arial", 12, "bold"), height=2, width=20)
        self.submit_btn.pack(pady=5)

        self.shuffle_btn = tk.Button(root, text="SHUFFLE TILES", command=self.shuffle_tiles, bg="blue", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.shuffle_btn.pack(pady=5)

        # Hint button starts dimmed
        self.hint_btn = tk.Button(root, text="GET HINT (-5 PTS)", command=self.give_hint, bg="gray", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.hint_btn.pack(pady=5)

        self.high_score_label = tk.Label(root, text=self.get_leaderboard_text(), fg="cyan", bg="#1a1a1a", font=("Arial", 10, "italic"))
        self.high_score_label.pack(side="bottom", pady=20)

        self.next_round()

    def play_sound(self):
        """Universal sound: Works on Mac and Replit/Linux"""
        try:
            # Try Mac sound first
            os.system('afplay /System/Library/Sounds/Ping.aiff &')
        except:
            # Fallback for Replit/Linux: Standard system beep
            print('\a')

    def next_round(self):
        self.target_word = random.choice(self.dictionary)
        self.info_label.config(text=f"The word has {len(self.target_word)} letters!")
        
        display_letters = list(self.target_word)
        while len(display_letters) < 8:
            display_letters.append(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        
        random.shuffle(display_letters)
        self.current_letters = display_letters
        self.refresh_tiles()

    def refresh_tiles(self):
        for widget in self.letter_frame.winfo_children():
            widget.destroy()
        for letter in self.current_letters:
            lbl = tk.Label(self.letter_frame, text=letter, font=("Arial", 20, "bold"),
                          width=2, relief="raised", bg="gold", fg="black")
            lbl.pack(side="left", padx=5)

    def shuffle_tiles(self):
        self.shuffle_btn.config(bg="lightblue")
        random.shuffle(self.current_letters)
        self.refresh_tiles()
        self.root.after(200, lambda: self.shuffle_btn.config(bg="blue"))

    def give_hint(self):
        if self.score >= 5:
            self.score -= 5
            self.update_ui()
            messagebox.showinfo("Hint", f"The word starts with: {self.target_word[0]}")
        else:
            messagebox.showwarning("No Points", "Score 5 points first to unlock hints!")

    def check_word(self):
        user_word = self.word_entry.get().upper().strip()
        self.word_entry.delete(0, tk.END)

        if user_word == self.target_word:
            self.play_sound()
            self.score += 10
            self.update_ui()
            messagebox.showinfo("Correct!", f"Well done! {self.target_word}")
            self.next_round()
        else:
            self.wrong_answer()

    def update_ui(self):
        self.score_label.config(text=f"POINTS: {self.score}")
        # Make hint button green if usable
        if self.score >= 5:
            self.hint_btn.config(bg="green", fg="white")
        else:
            self.hint_btn.config(bg="gray")

    def wrong_answer(self):
        self.lives -= 1
        self.lives_label.config(text="❤️" * self.lives)
        if self.lives <= 0:
            self.update_leaderboard()
            self.score = 0
            self.lives = 3
            self.update_ui()
            self.lives_label.config(text="❤️❤️❤️")
            self.next_round()
        else:
            messagebox.showerror("Wrong", "Keep trying!")

    def get_leaderboard_text(self):
        try:
            if os.path.exists("leaderboard.txt"):
                with open("leaderboard.txt", "r") as f:
                    return f"TOP SCORE: {f.read().strip()}"
        except:
            pass
        return "NO HIGH SCORE YET"

    def update_leaderboard(self):
        current_top = 0
        try:
            if os.path.exists("leaderboard.txt"):
                with open("leaderboard.txt", "r") as f:
                    data = f.read().split(" by ")
                    current_top = int(data[0])
        except:
            pass

        if self.score > current_top:
            with open("leaderboard.txt", "w") as f:
                f.write(f"{self.score} by {self.player_name}")
            messagebox.showinfo("New Record!", f"Legendary! {self.score} is the new high score!")
        else:
            messagebox.showinfo("Game Over", f"Final Score: {self.score}\nWord was: {self.target_word}")
        
        self.high_score_label.config(text=self.get_leaderboard_text())

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    name = simpledialog.askstring("Welcome", "Enter your name to play:")
    player = name if name else "Guest"
    root.deiconify()
    game = PidginScrabble(root, player)
    root.mainloop()