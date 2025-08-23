import tkinter as tk

def show_selection():
    indices = listbox.curselection()
    items = [listbox.get(i) for i in indices]
    lbl.config(text=f"Selected: {items}")

root = tk.Tk()
root.title("Listbox Demo")

listbox = tk.Listbox(root, selectmode="extended", height=6)
for item in ["Apple", "Banana", "Cherry", "Date", "Grapes", "Mango"]:
    listbox.insert("end", item)
listbox.pack(padx=10, pady=10)

tk.Button(root, text="Show", command=show_selection).pack()
lbl = tk.Label(root, text="Selected: []")
lbl.pack(pady=5)

root.mainloop()
