import tkinter as tk

def press(ch):
    if ch == "C":
        expr.set("")
    elif ch == "=":
        try:
            expr.set(str(eval(expr.get())))
        except Exception:
            expr.set("Error")
    else:
        expr.set(expr.get() + ch)

root = tk.Tk()
root.title("Calculator")

expr = tk.StringVar()

entry = tk.Entry(root, textvariable=expr, justify="right", font=("Consolas", 16))
entry.grid(row=0, column=0, columnspan=4, sticky="we", padx=5, pady=5)

buttons = [
    "7","8","9","/",
    "4","5","6","*",
    "1","2","3","-",
    "0",".","C","+",
    "="
]

r,c = 1,0
for b in buttons:
    if b == "=":
        tk.Button(root, text=b, width=9, command=lambda ch=b: press(ch)).grid(row=r, column=0, columnspan=4, sticky="we", padx=5, pady=5)
        break
    tk.Button(root, text=b, width=5, command=lambda ch=b: press(ch)).grid(row=r, column=c, padx=3, pady=3)
    c += 1
    if c == 4:
        r += 1
        c = 0

root.mainloop()
