import tkinter as tk
from tkinter import ttk
import time
import threading

def run_task():
    pb["value"] = 0
    for i in range(101):
        time.sleep(0.02)
        pb["value"] = i

root = tk.Tk()
root.title("Progressbar Demo")

pb = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate", maximum=100)
pb.pack(padx=10, pady=10)

tk.Button(root, text="Start", command=lambda: threading.Thread(target=run_task, daemon=True).start()).pack(pady=5)

root.mainloop()