import tkinter as tk

root = tk.Tk()
root.title("Layout Demo")

top = tk.Frame(root, bg="#f0f0f0")
top.pack(fill="x")

tk.Label(top, text="Name:").grid(row=0, column=0, padx=8, pady=8)
name = tk.Entry(top)
name.grid(row=0, column=1, padx=8, pady=8)

tk.Label(top, text="Email:").grid(row=1, column=0, padx=8, pady=8)
email = tk.Entry(top)
email.grid(row=1, column=1, padx=8, pady=8)

bottom = tk.Frame(root)
bottom.pack(fill="x", pady=10)
tk.Button(bottom, text="Submit").pack(side="left", padx=10)
tk.Button(bottom, text="Cancel", command=root.destroy).pack(side="right", padx=10)

root.mainloop()
