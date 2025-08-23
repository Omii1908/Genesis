import tkinter as tk
from tkinter import filedialog, messagebox

current_file = None

def new_file():
    global current_file
    current_file = None
    text.delete("1.0", "end")
    status.set("New file")

def open_file():
    global current_file
    path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All files", "*.*")])
    if not path: return
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text.delete("1.0", "end")
        text.insert("1.0", f.read())
    current_file = path
    status.set(f"Opened: {path}")

def save_file():
    global current_file
    if not current_file:
        save_as()
        return
    with open(current_file, "w", encoding="utf-8") as f:
        f.write(text.get("1.0", "end"))
    status.set(f"Saved: {current_file}")

def save_as():
    global current_file
    path = filedialog.asksaveasfilename(defaultextension=".txt")
    if not path: return
    current_file = path
    save_file()

root = tk.Tk()
root.title("Mini Editor")

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new_file)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_command(label="Save As", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

text = tk.Text(root, wrap="word", undo=True)
text.pack(expand=True, fill="both")

status = tk.StringVar(value="Ready")
tk.Label(root, textvariable=status, anchor="w").pack(fill="x")

root.mainloop()
