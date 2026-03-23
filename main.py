import random

def jumble_word(word):
    jumbled = list(word)
    random.shuffle(jumbled)
    return ''.join(jumbled)

def play_game():
    # Word list grouped by level (Easy, Medium, Hard)
    levels = {
        1: ["pikin", "sabi", "motto", "boku"],
        2: ["kakaki", "overtake", "wakabout", "bellefull"],
        3: ["confam", "expensiv", "ogbonge", "kpatakpata"]
    }
    
    score = 0
    current_level = 1
    
    print("--- 🎮 WELCOME TO PIDGIN JUMBLE: OGA EDITION 🎮 ---")
    
    while current_level <= 3:
        words = levels[current_level]
        random.shuffle(words)
        print(f"\n>>> LEVEL {current_level} START! <<<")
        
        for original in words:
            jumbled = jumble_word(original)
            print(f"\nJumbled Word: {jumbled}")
            guess = input("Wetin be the correct word? ").lower()
            
            if guess == original:
                score += (10 * current_level)
                print(f"Correct! Score: {score}")
            else:
                print(f"Oversabi! The correct word na: {original}")
        
        current_level += 1

    print(f"\nGAME OVER! Your Final Oga Score na: {score}")

if __name__ == "__main__":
    play_game()
