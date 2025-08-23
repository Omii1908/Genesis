import tkinter as tk

root = tk.Tk()
root.title("Canvas Drawing")

canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack(padx=10, pady=10)

canvas.create_rectangle(20, 20, 120, 80, fill="skyblue", outline="black")
canvas.create_oval(150, 30, 280, 160, fill="lightgreen", outline="darkgreen", width=2)
canvas.create_line(0, 0, 300, 200, fill="red", width=3)
canvas.create_text(150, 190, text="Shapes", font=("Arial", 12, "bold"))

root.mainloop()
