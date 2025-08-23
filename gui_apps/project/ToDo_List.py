import tkinter as tk
from tkinter import messagebox

def add_task():
    t = entry.get().strip()
    if t:
        lb.insert("end", t)
        entry.delete(0, "end")

def remove_task():
    sel = lb.curselection()
    if not sel:
        messagebox.showwarning("Select", "Select a task to remove")
        return
    lb.delete(sel[0])

def clear_all():
    if messagebox.askyesno("Confirm", "Clear all tasks?"):
        lb.delete(0, "end")

root = tk.Tk()
root.title("To-Do List")

entry = tk.Entry(root, width=30)
entry.grid(row=0, column=0, padx=5, pady=5, columnspan=2, sticky="we")

tk.Button(root, text="Add", command=add_task).grid(row=0, column=2, padx=5, pady=5)

scroll = tk.Scrollbar(root)
scroll.grid(row=1, column=3, sticky="ns")

lb = tk.Listbox(root, height=10, width=40, yscrollcommand=scroll.set)
lb.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="we")
scroll.config(command=lb.yview)

tk.Button(root, text="Remove Selected", command=remove_task).grid(row=2, column=0, pady=5)
tk.Button(root, text="Clear All", command=clear_all).grid(row=2, column=1, pady=5)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.mainloop()
