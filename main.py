import tkinter as tk
from map import run_map

# Main vindue
root = tk.Tk()
root.title("Main Menu")
root.geometry("300x250")

# Overskrift
label = tk.Label(root, text="Protect the Flag", font=("Arial", 14))
label.pack(pady=15)

# Knap til at åbne map
map_button = tk.Button(root, text="Åbn Map", command=run_map)
map_button.pack(pady=10)

root.mainloop()
