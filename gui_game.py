import tkinter as tk
from tkinter import messagebox
import random

class PidginScrabble:
    def __init__(self, root):
        self.root = root
        self.root.title("FRANK'S PIDGIN BUILDER PRO")
        self.root.geometry("500x700")
        self.root.configure(bg="#1a1a1a")
        self.dictionary = ["CHOP", "SABI", "WAHALA", "KOLO", "JARA", "OYIBO", "WEY", "BASH", "PIKIN", "VEX"]
        self.score, self.lives = 0, 3
        self.current_letters = []
        self.score_label = tk.Label(root, text="SCORE: 0", fg="gold", bg="#1a1a1a", font=("Arial", 24, "bold"))
        self.score_label.pack(pady=20)
        self.lives_label = tk.Label(root, text="❤️❤️❤️", fg="red", bg="#1a1a1a", font=("Arial", 18))
        self.lives_label.pack()
        self.rack_frame = tk.Frame(root, bg="#1a1a1a")
        self.rack_frame.pack(pady=40)
        self.word_entry = tk.Entry(root, font=("Arial", 24), justify='center', bg="#333", fg="white", insertbackground="white")
        self.word_entry.pack(pady=20, padx=50)
        self.word_entry.bind("<Return>", lambda e: self.check_word())
        tk.Button(root, text="SUBMIT", command=self.check_word, bg="gold", font=("Arial", 14, "bold")).pack()
        self.refresh_rack()

    def refresh_rack(self):
        for widget in self.rack_frame.winfo_children(): widget.destroy()
        self.current_letters = [random.choice("AEIOU") for _ in range(3)] + [random.choice("BCDFGHJKLMNPQRSTVWXYZ") for _ in range(4)]
        random.shuffle(self.current_letters)
        for letter in self.current_letters:
            tk.Label(self.rack_frame, text=letter, font=("Arial", 20, "bold"), width=2, bg="gold").pack(side="left", padx=5)

    def check_word(self):
        word = self.word_entry.get().upper().strip()
        temp_rack = self.current_letters.copy()
        valid = True
        for char in word:
            if char in temp_rack: temp_rack.remove(char)
            else: valid = False; break
        if valid and word in self.dictionary:
            self.score += len(word) * 10
            self.score_label.config(text=f"SCORE: {self.score}")
            self.refresh_rack()
        else:
            self.lives -= 1
            self.lives_label.config(text="❤️" * self.lives)
            if self.lives <= 0: messagebox.showinfo("Game Over", f"Score: {self.score}"); self.score, self.lives = 0, 3
        self.word_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PidginScrabble(root)
    root.mainloop()