import tkinter as tk

root = tk.Tk()
root.title("Text + Scrollbar")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

scroll = tk.Scrollbar(frame)
scroll.pack(side="right", fill="y")

txt = tk.Text(frame, wrap="word", yscrollcommand=scroll.set, width=40, height=10)
txt.pack(side="left", fill="both", expand=True)
scroll.config(command=txt.yview)

txt.insert("end", "Type multiple lines here...\nLine 2\nLine 3")

root.mainloop()
