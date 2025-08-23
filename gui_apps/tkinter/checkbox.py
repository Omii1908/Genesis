import tkinter as tk

def toggle():
    status.config(text=f"Subscribed: {var.get()==1}")

root = tk.Tk()
root.title("Checkbutton Demo")

var = tk.IntVar(value=0)
chk = tk.Checkbutton(root, text="Subscribe", variable=var, command=toggle)
chk.pack(padx=10, pady=10)

status = tk.Label(root, text="Subscribed: False")
status.pack(pady=5)

root.mainloop()
