import customtkinter as ctk
import random
import json
import os

class PidginBuilderPro:
    def __init__(self, root):
        self.root = root
        self.root.title("FRANK'S PIDGIN BUILDER PRO")
        self.root.geometry("500x700")
        self.root.configure(fg_color="#1a1a1a")
        
        # --- 1. DATA INITIALIZATION ---
        self.score_file = "high_scores.json"
        self.high_scores = self.load_scores()
        
        # --- 3. THE "MEGA" PIDGIN DICTIONARY ---
        self.pidgin_dict = [
            "sabi", "pikin", "chop", "oya", "biko", "massa", "wahala", "abeg", 
            "dash", "jara", "kolo", "magun", "ngwo", "obokun", "palava", 
            "quench", "runz", "shayo", "titi", "ununu", "voke", "wetin", 
            "yapa", "zanga", "akamu", "belle", "chei", "donatus", "efe",
            "fufu", "gari", "hanty", "isiewu", "jollof", "keke", "lappa",
            "mumu", "nne", "ogbono", "pepper", "suya", "ukwa", "vulture",
            "winch", "yabb", "zege", "afang", "boola", "comot", "domot"
        ]
        
        self.score = 0
        self.lives = 3
        self.current_rack = []
        
        self.setup_ui()
        self.new_round()

    def load_scores(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, "r") as f:
                    return json.load(f)
            except: return []
        return []

    def save_score(self, name):
        self.high_scores.append({"name": name, "score": self.score})
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:5]
        with open(self.score_file, "w") as f:
            json.dump(self.high_scores, f)

    def setup_ui(self):
        # Header
        self.title_label = ctk.CTkLabel(self.root, text="PIDGIN BUILDER PRO", font=("Impact", 35), text_color="#2ecc71")
        self.title_label.pack(pady=20)

        # Stats Row
        self.stats_label = ctk.CTkLabel(self.root, text=f"Score: 0  |  Lives: ❤️❤️❤️", font=("Arial", 20, "bold"))
        self.stats_label.pack(pady=10)

        # The Rack (Visual Polish - Golden Letters)
        self.rack_frame = ctk.CTkFrame(self.root, fg_color="#333333", corner_radius=10, border_width=2, border_color="#FFCC00")
        self.rack_frame.pack(pady=30, padx=20, fill="x")
        
        self.rack_label = ctk.CTkLabel(self.rack_frame, text="", font=("Courier New", 45, "bold"), text_color="#FFCC00")
        self.rack_label.pack(pady=15)

        # Input Area
        self.word_input = ctk.CTkEntry(self.root, placeholder_text="Type your word...", width=300, height=50, font=("Arial", 22), justify="center")
        self.word_input.pack(pady=10)
        self.word_input.bind("<Return>", lambda e: self.check_word())

        # Buttons
        self.submit_btn = ctk.CTkButton(self.root, text="SUBMIT WORD", command=self.check_word, fg_color="#27ae60", hover_color="#1e8449", font=("Arial", 18, "bold"), height=45)
        self.submit_btn.pack(pady=15)

        self.msg_label = ctk.CTkLabel(self.root, text="Build words from the letters above!", font=("Arial", 14), text_color="#aaaaaa")
        self.msg_label.pack(pady=5)

    def new_round(self):
        vowels = "AEIOU"
        consonants = "BCDFGHJKLMNPQRSTVWXYZ"
        # Always ensure at least 2 vowels for playable words
        self.current_rack = [random.choice(vowels) for _ in range(2)] + [random.choice(consonants) for _ in range(5)]
        random.shuffle(self.current_rack)
        self.rack_label.configure(text=" ".join(self.current_rack))
        self.word_input.delete(0, 'end')

    def check_word(self):
        user_word = self.word_input.get().lower().strip()
        if not user_word: return
        
        # 1. Check Dictionary
        if user_word in self.pidgin_dict:
            # 2. Check Rack (Scrabble Logic)
            rack_copy = self.current_rack.copy()
            match = True
            for char in user_word.upper():
                if char in rack_copy:
                    rack_copy.remove(char)
                else:
                    match = False
                    break
            
            if match:
                points = len(user_word) * 10
                self.score += points
                self.msg_label.configure(text=f"Correct! +{points} points", text_color="#2ecc71")
                self.update_stats()
                self.new_round()
            else:
                self.handle_wrong("Letters not in rack!")
        else:
            self.handle_wrong("Not in Pidgin dictionary!")

    def handle_wrong(self, reason):
        self.lives -= 1
        self.msg_label.configure(text=reason, text_color="#e74c3c")
        self.update_stats()
        if self.lives <= 0:
            self.game_over()
        else:
            self.new_round()

    def update_stats(self):
        lives_display = "❤️" * self.lives
        self.stats_label.configure(text=f"Score: {self.score}  |  Lives: {lives_display}")

    def game_over(self):
        # Leaderboard Pop-up
        dialog = ctk.CTkInputDialog(text=f"GAME OVER!\nFinal Score: {self.score}\nEnter name for Leaderboard:", title="Save Score")
        name = dialog.get_input()
        
        if name:
            self.save_score(name[:15]) # Limit name length
        
        # Show Top 5 on Screen
        leaderboard_text = "🏆 TOP 5 BUILDERS 🏆\n\n"
        for i, entry in enumerate(self.high_scores):
            leaderboard_text += f"{i+1}. {entry['name']}: {entry['score']}\n"
        
        self.rack_label.configure(text=leaderboard_text, font=("Arial", 18, "bold"), text_color="white")
        self.word_input.destroy()
        self.submit_btn.configure(text="PLAY AGAIN", command=self.restart_game)

    def restart_game(self):
        # Quick restart by rerunning the script
        os.system("python gui_game.py")
        self.root.destroy()

if __name__ == "__main__":
    app = ctk.CTk()
    PidginBuilderPro(app)
    app.mainloop()