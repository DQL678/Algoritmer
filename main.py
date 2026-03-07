import tkinter as tk
from map import run_map
from game_manager import GameManager

game_manager = GameManager()

def open_difficulty_window():
    difficulty_window = tk.Toplevel(root)
    difficulty_window.title("Difficulty Settings")
    difficulty_window.geometry("250x180")

    title = tk.Label(difficulty_window, text="Choose Difficulty", font=("Arial", 12))
    title.pack(pady=10)

    selected_difficulty = tk.StringVar(value=game_manager.get_difficulty())

    easy_button = tk.Radiobutton(
        difficulty_window,
        text="Easy (BFS)",
        variable=selected_difficulty,
        value="easy"
    )
    easy_button.pack(pady=5)

    hard_button = tk.Radiobutton(
        difficulty_window,
        text="Hard (A*)",
        variable=selected_difficulty,
        value="hard"
    )
    hard_button.pack(pady=5)

    def save_difficulty():
        game_manager.set_difficulty(selected_difficulty.get())
        difficulty_window.destroy()

    save_button = tk.Button(difficulty_window, text="Save", command=save_difficulty)
    save_button.pack(pady=15)

def start_game():
    run_map(game_manager.get_difficulty())

root = tk.Tk()
root.title("Main Menu")
root.geometry("300x250")

label = tk.Label(root, text="Protect the Flag", font=("Arial", 14))
label.pack(pady=15)

difficulty_button = tk.Button(root, text="Difficulty Settings", command=open_difficulty_window)
difficulty_button.pack(pady=10)

map_button = tk.Button(root, text="Start Game", command=start_game)
map_button.pack(pady=10)

root.mainloop()