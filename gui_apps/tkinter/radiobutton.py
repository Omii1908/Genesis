import tkinter as tk

def update():
    lbl.config(text=f"Selected: {choice.get()}")

root = tk.Tk()
root.title("Radiobutton Demo")

choice = tk.StringVar(value="Python")
for lang in ["Python", "Java", "C++"]:
    tk.Radiobutton(root, text=lang, value=lang, variable=choice, command=update).pack(anchor="w")

lbl = tk.Label(root, text="Selected: Python")
lbl.pack(pady=5)

root.mainloop()
