import tkinter as tk
from tkinter import ttk, messagebox

def add_expense():
    try:
        amt = float(amount.get())
    except ValueError:
        messagebox.showerror("Invalid", "Amount must be a number")
        return
    cat = category.get().strip() or "Other"
    note = desc.get().strip()
    tv.insert("", "end", values=(f"{amt:.2f}", cat, note))
    amount.delete(0, "end")
    desc.delete(0, "end")
    update_total()

def delete_selected():
    for sel in tv.selection():
        tv.delete(sel)
    update_total()

def update_total():
    total = 0.0
    for child in tv.get_children():
        total += float(tv.item(child, "values"))
    total_var.set(f"Total: {total:.2f}")

root = tk.Tk()
root.title("Expense Tracker")

tk.Label(root, text="Amount").grid(row=0, column=0, padx=5, pady=5, sticky="e")
amount = tk.Entry(root, width=12)
amount.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Category").grid(row=0, column=2, padx=5, pady=5, sticky="e")
category = ttk.Combobox(root, values=["Food", "Transport", "Bills", "Shopping", "Other"], width=12, state="readonly")
category.current(0)
category.grid(row=0, column=3, padx=5, pady=5)

tk.Label(root, text="Note").grid(row=1, column=0, padx=5, pady=5, sticky="e")
desc = tk.Entry(root, width=30)
desc.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")

ttk.Button(root, text="Add", command=add_expense).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(root, text="Delete", command=delete_selected).grid(row=2, column=1, padx=5, pady=5)

cols = ("Amount", "Category", "Note")
tv = ttk.Treeview(root, columns=cols, show="headings", height=8)
for c in cols: tv.heading(c, text=c)
tv.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

total_var = tk.StringVar(value="Total: 0.00")
tk.Label(root, textvariable=total_var, anchor="w").grid(row=4, column=0, columnspan=4, sticky="we", padx=5, pady=5)

for i in range(4): root.grid_columnconfigure(i, weight=1)
root.grid_rowconfigure(3, weight=1)

root.mainloop()
