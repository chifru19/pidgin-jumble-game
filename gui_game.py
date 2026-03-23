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
        
        # This line forces the window to pop up in front of VS Code
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

        self.submit_btn = tk.Button(root, text="SUBMIT WORD", command=self.check_word, bg="gold", font=("Arial", 12, "bold"), height=2, width=20)
        self.submit_btn.pack(pady=5)

        self.shuffle_btn = tk.Button(root, text="SHUFFLE TILES", command=self.shuffle_tiles, bg="blue", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.shuffle_btn.pack(pady=5)

        self.hint_btn = tk.Button(root, text="GET HINT (-5 PTS)", command=self.give_hint, bg="red", fg="white", font=("Arial", 12, "bold"), height=2, width=20)
        self.hint_btn.pack(pady=5)

        self.high_score_label = tk.Label(root, text=self.get_leaderboard_text(), fg="cyan", bg="#1a1a1a", font=("Arial", 10, "italic"))
        self.high_score_label.pack(side="bottom", pady=20)

        self.next_round()

    def play_sound(self):
        os.system('afplay /System/Library/Sounds/Ping.aiff &')

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
        random.shuffle(self.current_letters)
        self.refresh_tiles()

    def give_hint(self):
        if self.score == 0:
            messagebox.showinfo("First Hint Free", f"Starts with: {self.target_word[0]}")
            return
        if self.score >= 5:
            self.score -= 5
            self.score_label.config(text=f"POINTS: {self.score}")
            messagebox.showinfo("Hint", f"Starts with: {self.target_word[0]}")
        else:
            messagebox.showwarning("No Points", "Oga, get 5 points first!")

    def check_word(self):
        user_word = self.word_entry.get().upper().strip()
        self.word_entry.delete(0, tk.END)

        if user_word == self.target_word:
            self.play_sound()
            self.score += 10
            self.score_label.config(text=f"POINTS: {self.score}")
            messagebox.showinfo("Correct!", f"Correct!