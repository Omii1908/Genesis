import tkinter as tk

root = tk.Tk()
root.title("Basic Window")

label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16))
label.pack(padx=20, pady=20)

root.mainloop()