import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import statistics

class StudentScoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Score Tracker")

        # Top form
        form = tk.LabelFrame(root, text="Add Record")
        form.pack(fill="x", padx=10, pady=8)

        tk.Label(form, text="Name").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        tk.Label(form, text="Subject").grid(row=0, column=2, padx=6, pady=6, sticky="e")
        tk.Label(form, text="Score (0-100)").grid(row=0, column=4, padx=6, pady=6, sticky="e")

        self.name_var = tk.StringVar()
        self.subj_var = tk.StringVar()
        self.score_var = tk.StringVar()

        tk.Entry(form, textvariable=self.name_var, width=20).grid(row=0, column=1, padx=6, pady=6)
        ttk.Combobox(form, textvariable=self.subj_var, values=[
            "Math", "Science", "English", "Computer", "History"
        ], state="readonly", width=18).grid(row=0, column=3, padx=6, pady=6)
        tk.Entry(form, textvariable=self.score_var, width=10).grid(row=0, column=5, padx=6, pady=6)

        tk.Button(form, text="Add", command=self.add_record).grid(row=0, column=6, padx=8, pady=6)

        # Search/filter
        filter_frame = tk.LabelFrame(root, text="Filter")
        filter_frame.pack(fill="x", padx=10, pady=4)

        tk.Label(filter_frame, text="Name contains").grid(row=0, column=0, padx=6, pady=6)
        tk.Label(filter_frame, text="Subject").grid(row=0, column=2, padx=6, pady=6)

        self.filter_name = tk.StringVar()
        self.filter_subj = tk.StringVar()

        tk.Entry(filter_frame, textvariable=self.filter_name, width=20).grid(row=0, column=1, padx=6, pady=6)
        ttk.Combobox(filter_frame, textvariable=self.filter_subj, values=[
            "", "Math", "Science", "English", "Computer", "History"
        ], state="readonly", width=18).grid(row=0, column=3, padx=6, pady=6)

        tk.Button(filter_frame, text="Apply", command=self.apply_filter).grid(row=0, column=4, padx=6)
        tk.Button(filter_frame, text="Clear", command=self.clear_filter).grid(row=0, column=5, padx=6)

        # Table
        table_frame = tk.Frame(root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=4)

        cols = ("Name", "Subject", "Score")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c)
            width = 160 if c != "Score" else 100
            self.tree.column(c, width=width, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Bottom actions
        action = tk.Frame(root)
        action.pack(fill="x", padx=10, pady=4)

        tk.Button(action, text="Delete Selected", command=self.delete_selected).pack(side="left", padx=4)
        tk.Button(action, text="Compute Stats", command=self.compute_stats).pack(side="left", padx=4)
        tk.Button(action, text="Save CSV", command=self.save_csv).pack(side="left", padx=4)
        tk.Button(action, text="Load CSV", command=self.load_csv).pack(side="left", padx=4)

        self.status = tk.Label(root, text="Ready", anchor="w")
        self.status.pack(fill="x", padx=10, pady=6)

        # Store full data separately for filtering
        self.data = []  # list of dicts: {"name":..., "subject":..., "score": int}

    def add_record(self):
        name = self.name_var.get().strip()
        subject = self.subj_var.get().strip()
        score_str = self.score_var.get().strip()

        if not name:
            messagebox.showwarning("Validation", "Name is required.")
            return
        if not subject:
            messagebox.showwarning("Validation", "Subject is required.")
            return
        try:
            score = int(score_str)
            if not (0 <= score <= 100):
                raise ValueError
        except Exception:
            messagebox.showwarning("Validation", "Score must be an integer between 0 and 100.")
            return

        rec = {"name": name, "subject": subject, "score": score}
        self.data.append(rec)
        self.refresh_table(self.data)
        self.clear_form()
        self.status.config(text=f"Added: {name}, {subject}, {score}")

    def clear_form(self):
        self.name_var.set("")
        self.subj_var.set("")
        self.score_var.set("")

    def refresh_table(self, rows):
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert
        for r in rows:
            self.tree.insert("", "end", values=(r["name"], r["subject"], r["score"]))

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            self.status.config(text="No selection to delete.")
            return
        # Get values and remove from data
        to_delete = []
        for iid in selected:
            vals = self.tree.item(iid, "values")
            to_delete.append((vals[0], vals, int(vals)))

        # Remove matching entries from self.data
        for name, subject, score in to_delete:
            for i, rec in enumerate(self.data):
                if rec["name"] == name and rec["subject"] == subject and rec["score"] == score:
                    self.data.pop(i)
                    break

        self.refresh_table(self.data)
        self.status.config(text=f"Deleted {len(to_delete)} record(s).")

    def compute_stats(self):
        if not self.data:
            messagebox.showinfo("Stats", "No data to compute.")
            return
        scores = [r["score"] for r in self.data]
        avg = round(statistics.mean(scores), 2)
        mn = min(scores)
        mx = max(scores)
        messagebox.showinfo("Stats", f"Average: {avg}\nMin: {mn}\nMax: {mx}")
        self.status.config(text=f"Stats computed: avg={avg}, min={mn}, max={mx}")

    def apply_filter(self):
        name_part = self.filter_name.get().strip().lower()
        subj = self.filter_subj.get().strip()
        filtered = []
        for r in self.data:
            if name_part and name_part not in r["name"].lower():
                continue
            if subj and r["subject"] != subj:
                continue
            filtered.append(r)
        self.refresh_table(filtered)
        self.status.config(text=f"Filter applied: {len(filtered)} record(s)")

    def clear_filter(self):
        self.filter_name.set("")
        self.filter_subj.set("")
        self.refresh_table(self.data)
        self.status.config(text="Filter cleared.")

    def save_csv(self):
        if not self.data:
            messagebox.showinfo("Save", "No data to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files","*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Subject", "Score"])
            for r in self.data:
                writer.writerow([r["name"], r["subject"], r["score"]])
        self.status.config(text=f"Saved to {path}")

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files","*.csv")])
        if not path:
            return
        try:
            loaded = []
            with open(path, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Validate each row
                    name = row.get("Name","").strip()
                    subject = row.get("Subject","").strip()
                    score_str = row.get("Score","").strip()
                    if not name or not subject:
                        continue
                    try:
                        score = int(score_str)
                        if not (0 <= score <= 100):
                            continue
                    except Exception:
                        continue
                    loaded.append({"name": name, "subject": subject, "score": score})
            self.data = loaded
            self.refresh_table(self.data)
            self.status.config(text=f"Loaded {len(self.data)} record(s) from {path}")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentScoreApp(root)
    root.mainloop()
