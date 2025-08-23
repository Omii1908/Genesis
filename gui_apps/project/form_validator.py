import tkinter as tk
from tkinter import messagebox
import re

def submit():
    email = e_email.get().strip()
    pwd = e_pwd.get()
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        messagebox.showerror("Invalid", "Enter a valid email")
        return
    if len(pwd) < 6:
        messagebox.showwarning("Weak", "Password should be at least 6 chars")
        return
    messagebox.showinfo("Success", "Form submitted!")

root = tk.Tk()
root.title("Form Validator")

tk.Label(root, text="Email").grid(row=0, column=0, sticky="e", padx=5, pady=5)
e_email = tk.Entry(root, width=30)
e_email.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Password").grid(row=1, column=0, sticky="e", padx=5, pady=5)
e_pwd = tk.Entry(root, show="*", width=30)
e_pwd.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Submit", command=submit).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
