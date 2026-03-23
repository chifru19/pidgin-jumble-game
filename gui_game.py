import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class PidginBuilderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("FRANK'S PIDGIN BUILDER PRO")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")

        # 1. DATA & DICTIONARY
        self.score = 0
        self.lives = 3
        self.dictionary = ["CHOP", "SABI", "WAHALA", "KOLO", "JARA", "OYIBO", "WEY", "BASH", "ZANGA", "GBEDU"]
        
        # 2. UI HEADER
        self.score_label = tk.Label(root, text=f"SCORE: {self.score}", fg="gold", bg="#1a1a1a", font=("Arial", 20, "bold"))
        self.score_label.pack(pady=20)

        self.lives_label = tk.Label(root, text="❤️" * self.lives, fg="red", bg="#1a1a1a", font=("Arial", 16))
        self.lives_label.pack()

        # 3. THE RACK (Letters Display)
        self.rack_frame = tk.Frame(root, bg="#1a1a1a")
        self.rack_frame.pack(pady=30)
        self.current_letters = []
        self.refresh_rack()

        # 4. INPUT
        self.word_entry = tk.Entry(root, font=("Arial", 24), justify='center', bg="#333", fg="white", insertbackground="white")
        self.word_entry.pack(pady=20, padx=50)
        self.word_entry.bind("<Return>", lambda e: self.check_word())

        self.btn = tk.Button(root, text="SUBMIT WORD", command=self.check_word, bg="gold", fg="black", font=("Arial", 14, "bold"), width=15)
        self.btn.pack(pady=10)

    def refresh_rack(self):
        for widget in self.rack_frame.winfo_children():
            widget.destroy()
        self.current_letters = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(7)]
        for letter in self.current_letters:
            lbl = tk.Label(self.rack_frame, text=letter, font=("Arial", 18, "bold"), width=2, relief="raised", bg="gold", fg="black")
            lbl.pack(side="left", padx=5)

    def check_word(self):
        word = self.word_entry.get().upper()
        if not word: return
        
        if word in self.dictionary:
            self.score += len(word) * 10
            self.score_label.config(text=f"SCORE: {self.score}")
            self.word_entry.delete(0, tk.END)
            self.refresh_rack()
        else:
            self.lives -= 1
            self.lives_label.config(text="❤️" * self.lives)
            messagebox.showwarning("OYO!", f"{word} no dey dictionary!")
            self.word_entry.delete(0, tk.END)
            if self.lives <= 0:
                messagebox.showinfo("GAME OVER", f"Final Score: {self.score}")
                self.score = 0
                self.lives = 3
                self.refresh_rack()
                self.score_label.config(text="SCORE: 0")
                self.lives_label.config(text="❤️❤️❤️")

if __name__ == "__main__":
    root = tk.Tk()
    app = PidginBuilderPro(root)
    root.mainloop()