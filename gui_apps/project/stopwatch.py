import tkinter as tk
import time

running = False
start_ts = 0
elapsed = 0

def update_clock():
    if running:
        now = time.time()
        t = elapsed + (now - start_ts)
        lbl_var.set(time.strftime("%M:%S", time.gmtime(t)) + f".{int((t%1)*100):02d}")
        root.after(30, update_clock)

def start():
    global running, start_ts
    if not running:
        running = True
        start_ts = time.time()
        update_clock()

def stop():
    global running, elapsed
    if running:
        running = False
        elapsed += time.time() - start_ts

def reset():
    global running, elapsed
    running = False
    elapsed = 0
    lbl_var.set("00:00.00")

root = tk.Tk()
root.title("Stopwatch")

lbl_var = tk.StringVar(value="00:00.00")
tk.Label(root, textvariable=lbl_var, font=("Consolas", 24)).pack(pady=10)

tk.Button(root, text="Start", command=start).pack(side="left", padx=10, pady=10)
tk.Button(root, text="Stop", command=stop).pack(side="left", padx=10, pady=10)
tk.Button(root, text="Reset", command=reset).pack(side="left", padx=10, pady=10)

root.mainloop()
