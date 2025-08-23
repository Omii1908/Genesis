import tkinter as tk

def on_click():
    btn.config(text="Clicked!")

root = tk.Tk()
root.title("Button Demo")

btn = tk.Button(root, text="Click me", command=on_click)
btn.pack(padx=20, pady=20)

root.mainloop()
