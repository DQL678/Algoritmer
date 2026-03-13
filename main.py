import tkinter as tk
import pygame
from map import run_map
from game_manager import GameManager

game_manager = GameManager()

music_on = False

# Prøv at starte musik sikkert
try:
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    music_on = True
except pygame.error:
    print("Kunne ikke starte lydsystemet.")


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


def open_sound_window():
    sound_window = tk.Toplevel(root)
    sound_window.title("Sound Settings")
    sound_window.geometry("300x220")

    title = tk.Label(sound_window, text="Music Settings", font=("Arial", 12))
    title.pack(pady=10)

    if music_on:
        current_volume = int(pygame.mixer.music.get_volume() * 100)
    else:
        current_volume = 40

    volume_label = tk.Label(sound_window, text=f"Volume: {current_volume}%")
    volume_label.pack(pady=5)

    def change_volume(value):
        if music_on:
            volume = float(value) / 100
            pygame.mixer.music.set_volume(volume)
        volume_label.config(text=f"Volume: {int(float(value))}%")

    volume_slider = tk.Scale(
        sound_window,
        from_=0,
        to=100,
        orient="horizontal",
        command=change_volume
    )
    volume_slider.set(current_volume)
    volume_slider.pack(pady=10)

    def start_music():
        global music_on
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            pygame.mixer.music.load("output.mp3")
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(volume_slider.get() / 100)
            music_on = True
        except pygame.error:
            print("Kunne ikke starte musik.")

    def stop_music():
        global music_on
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
        music_on = False

    start_button = tk.Button(sound_window, text="Start Music", command=start_music)
    start_button.pack(pady=5)

    stop_button = tk.Button(sound_window, text="Stop Music", command=stop_music)
    stop_button.pack(pady=5)


def start_game():
    game_manager.set_creative_mode(False)
    run_map(game_manager)


def start_creative_mode():
    game_manager.set_creative_mode(True)
    run_map(game_manager)


root = tk.Tk()
root.title("Main Menu")
root.geometry("300x360")

label = tk.Label(root, text="Protect the Flag", font=("Arial", 14))
label.pack(pady=15)

difficulty_button = tk.Button(root, text="Difficulty Settings", command=open_difficulty_window)
difficulty_button.pack(pady=10)

sound_button = tk.Button(root, text="Sound Settings", command=open_sound_window)
sound_button.pack(pady=10)

map_button = tk.Button(root, text="Start Game", command=start_game)
map_button.pack(pady=10)

creative_button = tk.Button(root, text="Creative Mode", command=start_creative_mode)
creative_button.pack(pady=10)

root.mainloop()