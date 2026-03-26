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
        
        # Game Data
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

        # Added a specific Hint Display label so it shows on screen
        self.hint_display = tk.Label(root, text="", fg="#00FF00", bg="#1a1a1a", font=("Arial", 14, "italic"))
        self.hint_display.pack(pady=5)

        self.info_label = tk.Label(root, text="Loading...", fg="white", bg="#1a1a1a", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.letter_frame = tk.Frame(root, bg="#1a1a1a")
        self.letter_frame.pack(pady=30, fill="x")

        self.word_entry = tk.Entry(root, font=("Arial", 22), justify='center', bg="#333", fg="white", 
                                  insertbackground="white", borderwidth=0, highlightthickness=1)
        self.word_entry.pack(pady=15, ipady=10, padx=50)
        self.word_entry.focus_set()
        self.word_entry.bind("<Return>", lambda event: self.check_word())

        # Button Styling
        self.submit_btn = tk.Button(root, text="SUBMIT WORD", command=self.check_word, bg="#28a745", 
                                   fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.submit_btn.pack(pady=5)

        self.shuffle_btn = tk.Button(root, text="SHUFFLE TILES", command=self.shuffle_tiles, bg="#0056b3", 
                                    fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.shuffle_btn.pack(pady=5)

        self.hint_btn = tk.Button(root, text="GET HINT (-5 PTS)", command=self.give_hint, bg="#555", 
                                 fg="white", font=("Arial", 12, "bold"), height=2, width=22)
        self.hint_btn.pack(pady=5)

        self.high_score_label = tk.Label(root, text=self.get_leaderboard_text(), fg="cyan", bg="#1a1a1a", font=("Arial", 11, "italic"))
        self.high_score_label.pack(side="bottom", pady=30)

        self.next_round()

    def next_round(self):
        self.target_word = random.choice(self.dictionary)
        self.hint_display.config(text="") # Clear hint for new round
        self.info_label.config(text=f"The word has {len(self.target_word)} letters!")
        
        display_letters = list(self.target_word)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for _ in range(2): # Distractor tiles