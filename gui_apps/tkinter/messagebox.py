import tkinter as tk
from tkinter import messagebox

def confirm():
    ans = messagebox.askyesno("Confirm", "Proceed?")
    lbl.config(text=f"Answer: {ans}")

root = tk.Tk()
root.title("Messagebox Demo")

tk.Button(root, text="Ask", command=confirm).pack(padx=10, pady=10)
lbl = tk.Label(root, text="Answer: ")
lbl.pack(pady=5)

root.mainloop()
