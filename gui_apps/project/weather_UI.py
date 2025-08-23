import tkinter as tk
from tkinter import ttk

MOCK = {
    "Kolkata": {"temp": 31, "cond": "Humid"},
    "Ranchi": {"temp": 27, "cond": "Cloudy"},
    "Mumbai": {"temp": 29, "cond": "Rain"},
}

def fetch():
    city = cb.get()
    data = MOCK.get(city, {"temp": "-", "cond": "-"})
    temp.set(f"{data['temp']} °C")
    cond.set(data["cond"])

root = tk.Tk()
root.title("Weather (Mock)")

tk.Label(root, text="City:").grid(row=0, column=0, padx=6, pady=6)
cb = ttk.Combobox(root, values=list(MOCK.keys()), state="readonly")
cb.current(0)
cb.grid(row=0, column=1, padx=6, pady=6)

ttk.Button(root, text="Fetch", command=fetch).grid(row=0, column=2, padx=6, pady=6)

temp = tk.StringVar(value="-")
cond = tk.StringVar(value="-")
ttk.Label(root, text="Temperature:").grid(row=1, column=0, sticky="e")
ttk.Label(root, textvariable=temp).grid(row=1, column=1, sticky="w")
ttk.Label(root, text="Condition:").grid(row=2, column=0, sticky="e")
ttk.Label(root, textvariable=cond).grid(row=2, column=1, sticky="w")

root.mainloop()
