import tkinter as tk

def say(msg):
    status.config(text=msg)

root = tk.Tk()
root.title("Menu Demo")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=lambda: say("New clicked"))
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda: say("Tkinter Menu Demo v1.0"))
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

status = tk.Label(root, text="Ready", anchor="w")
status.pack(fill="x", padx=10, pady=10)

root.mainloop()
