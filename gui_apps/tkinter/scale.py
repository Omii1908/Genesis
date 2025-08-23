import tkinter as tk

def changed(val):
    lbl.config(text=f"Value: {scale.get()}")

root = tk.Tk()
root.title("Scale Demo")

scale = tk.Scale(root, from_=0, to=100, orient="horizontal", command=changed)
scale.pack(padx=10, pady=10)

lbl = tk.Label(root, text="Value: 0")
lbl.pack(pady=5)

root.mainloop()
