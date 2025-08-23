import tkinter as tk
from tkinter import ttk

def on_select(event=None):
    lbl.config(text=f"Chosen: {combo.get()}")

root = tk.Tk()
root.title("Combobox Demo")

combo = ttk.Combobox(root, values=["Beginner", "Intermediate", "Advanced"], state="readonly")
combo.current(0)
combo.pack(padx=10, pady=10)
combo.bind("<<ComboboxSelected>>", on_select)

lbl = tk.Label(root, text="Chosen: Beginner")
lbl.pack(pady=5)

root.mainloop()
