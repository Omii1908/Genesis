import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview Demo")

cols = ("Name", "Age", "City")
tree = ttk.Treeview(root, columns=cols, show="headings", height=6)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=120)
tree.pack(padx=10, pady=10)

data = [
    ("Anita", 23, "Kolkata"),
    ("Rahul", 25, "Ranchi"),
    ("Meera", 22, "Delhi"),
]
for row in data:
    tree.insert("", "end", values=row)

root.mainloop()
