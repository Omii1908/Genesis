import tkinter as tk

def show_text():
    out.config(text=f"You typed: {ent.get()}")

root = tk.Tk()
root.title("Entry Demo")

ent = tk.Entry(root, width=30)
ent.pack(padx=10, pady=10)

tk.Button(root, text="Show", command=show_text).pack(pady=5)
out = tk.Label(root, text="")
out.pack(pady=5)

root.mainloop()
