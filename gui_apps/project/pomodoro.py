import tkinter as tk

WORK_SEC = 25*60
BREAK_SEC = 5*60

running = False
remaining = WORK_SEC
on_break = False

def tick():
    global remaining, running, on_break
    if not running: return
    if remaining > 0:
        remaining -= 1
        mins, secs = divmod(remaining, 60)
        time_var.set(f"{mins:02d}:{secs:02d}")
        root.after(1000, tick)
    else:
        on_break = not on_break
        remaining = BREAK_SEC if on_break else WORK_SEC
        status_var.set("Break" if on_break else "Work")
        tick()

def start():
    global running
    if not running:
        running = True
        tick()

def pause():
    global running
    running = False

def reset():
    global running, remaining, on_break
    running = False
    on_break = False
    remaining = WORK_SEC
    time_var.set("25:00")
    status_var.set("Work")

root = tk.Tk()
root.title("Pomodoro")

status_var = tk.StringVar(value="Work")
time_var = tk.StringVar(value="25:00")

tk.Label(root, textvariable=status_var, font=("Arial", 16)).pack(pady=5)
tk.Label(root, textvariable=time_var, font=("Consolas", 32)).pack(pady=10)

tk.Button(root, text="Start", command=start).pack(side="left", padx=5, pady=10)
tk.Button(root, text="Pause", command=pause).pack(side="left", padx=5, pady=10)
tk.Button(root, text="Reset", command=reset).pack(side="left", padx=5, pady=10)

root.mainloop()
