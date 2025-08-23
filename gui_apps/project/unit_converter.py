import tkinter as tk
from tkinter import ttk, messagebox

def convert():
    try:
        val = float(entry.get())
        if mode.get() == "C2F":
            res = (val * 9/5) + 32
            out.set(f"{val:.2f} °C = {res:.2f} °F")
        else:
            res = (val - 32) * 5/9
            out.set(f"{val:.2f} °F = {res:.2f} °C")
    except ValueError:
        messagebox.showerror("Invalid", "Please enter a valid number")

root = tk.Tk()
root.title("Unit Converter")

tk.Label(root, text="Value:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
entry = tk.Entry(root, width=15)
entry.grid(row=0, column=1, padx=8, pady=8)

mode = tk.StringVar(value="C2F")
ttk.Radiobutton(root, text="Celsius → Fahrenheit", variable=mode, value="C2F").grid(row=1, column=0, columnspan=2, sticky="w", padx=8)
ttk.Radiobutton(root, text="Fahrenheit → Celsius", variable=mode, value="F2C").grid(row=2, column=0, columnspan=2, sticky="w", padx=8)

ttk.Button(root, text="Convert", command=convert).grid(row=3, column=0, columnspan=2, pady=8)
out = tk.StringVar(value="Result will appear here")
ttk.Label(root, textvariable=out).grid(row=4, column=0, columnspan=2, pady=8)

root.mainloop()
