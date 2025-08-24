import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import time
import difflib

APP_TITLE = "AI & Data Science Quiz"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

CATEGORIES = {
    "AI Fundamentals": os.path.join(DATA_DIR, "questions_ai.json"),
    "Machine Learning": os.path.join(DATA_DIR, "questions_ml.json"),
    "Deep Learning": os.path.join(DATA_DIR, "questions_dl.json"),
    "Data Science": os.path.join(DATA_DIR, "questions_ds.json"),
}

DEFAULT_SETTINGS = {
    "time_per_question_sec": 30,   # per-question timer
    "num_questions": 5,            # number to sample (if available)
    "shuffle": True
}

def load_questions(path):
    with open(path, "r", encoding="utf-8") as f:
        qs = json.load(f)
    # normalize fields
    normalized = []
    for q in qs:
        item = {
            "id": q.get("id"),
            "type": q.get("type", "mcq"),
            "question": q.get("question", "").strip(),
            "options": q.get("options", []),
            "answer": q.get("answer", "").strip(),
            "aliases": [a.strip().lower() for a in q.get("aliases", [])],
            "explanation": q.get("explanation", "").strip()
        }
        normalized.append(item)
    return normalized

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fuzzy_match(user_text, correct, aliases=None, cutoff=0.8):
    if not user_text:
        return False
    user = user_text.strip().lower()
    corrects = [correct.strip().lower()] if correct else []
    if aliases:
        corrects.extend([a.strip().lower() for a in aliases])
    # exact
    if user in corrects:
        return True
    # fuzzy
    scores = [difflib.SequenceMatcher(None, user, c).ratio() for c in corrects]
    return max(scores) >= cutoff if scores else False

class QuizEngine:
    def __init__(self, questions, settings):
        self.all_questions = questions[:]
        self.settings = settings
        self.reset()

    def reset(self):
        import random
        self.index = 0
        self.correct = 0
        self.start_time = time.time()
        self.answers = []  # list of dict: {id, user_answer, correct_answer, is_correct, time_taken}
        self.order = list(range(len(self.all_questions)))
        if self.settings.get("shuffle", True):
            random.shuffle(self.order)
        n = self.settings.get("num_questions", len(self.all_questions))
        n = min(n, len(self.all_questions))
        self.order = self.order[:n]
        self.per_question_time = self.settings.get("time_per_question_sec", 30)
        self.deadline = time.time() + self.per_question_time if n > 0 else None

    def has_next(self):
        return self.index < len(self.order)

    def current_question(self):
        if not self.has_next():
            return None
        q = self.all_questions[self.order[self.index]]
        return q

    def submit_answer(self, user_answer):
        q = self.current_question()
        if q is None:
            return
        now = time.time()
        time_taken = self.settings.get("time_per_question_sec", 30) - max(0, int(self.deadline - now)) if self.deadline else 0

        is_correct = False
        if q["type"] == "mcq":
            is_correct = (user_answer == q["answer"])
        else:
            is_correct = fuzzy_match(user_answer, q["answer"], q.get("aliases", []))

        if is_correct:
            self.correct += 1

        self.answers.append({
            "id": q["id"],
            "question": q["question"],
            "type": q["type"],
            "options": q.get("options", []),
            "user_answer": user_answer,
            "correct_answer": q["answer"],
            "is_correct": bool(is_correct),
            "explanation": q.get("explanation", ""),
            "time_taken_sec": time_taken
        })

        self.index += 1
        if self.has_next():
            self.deadline = time.time() + self.per_question_time

    def time_left(self):
        if not self.deadline:
            return 0
        return max(0, int(self.deadline - time.time()))

    def forced_timeout(self):
        # submit empty or None if time up
        self.submit_answer("")

    def summary(self):
        total = len(self.order)
        accuracy = (self.correct / total * 100.0) if total else 0.0
        elapsed = int(time.time() - self.start_time)
        return {
            "total": total,
            "correct": self.correct,
            "accuracy": round(accuracy, 2),
            "elapsed_sec": elapsed
        }

class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        icon_path = os.path.join(ASSETS_DIR, "icon.png")
        if os.path.exists(icon_path):
            try:
                icon_img = tk.PhotoImage(file=icon_path)
                self.iconphoto(True, icon_img)
            except Exception:
                pass

        self.geometry("800x540")
        self.resizable(True, True)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.questions_by_category = {}
        self.load_all_categories()

        self.engine = None
        self.settings = DEFAULT_SETTINGS.copy()
        self.category_var = tk.StringVar(value=list(CATEGORIES.keys())[0])
        self.view = None

        self.build_menu()
        self.show_home()

    def load_all_categories(self):
        for name, path in CATEGORIES.items():
            try:
                self.questions_by_category[name] = load_questions(path)
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load {name}: {e}")
                self.questions_by_category[name] = []

    def build_menu(self):
        mbar = tk.Menu(self)
        # File
        m_file = tk.Menu(mbar, tearoff=0)
        m_file.add_command(label="Import Questions (JSON)", command=self.import_questions)
        m_file.add_command(label="Export Session (JSON)", command=self.export_session)
        m_file.add_separator()
        m_file.add_command(label="Exit", command=self.on_close)
        mbar.add_cascade(label="File", menu=m_file)
        # Settings
        m_settings = tk.Menu(mbar, tearoff=0)
        m_settings.add_command(label="Quiz Settings", command=self.show_settings)
        mbar.add_cascade(label="Settings", menu=m_settings)
        # Help
        m_help = tk.Menu(mbar, tearoff=0)
        m_help.add_command(label="About", command=self.show_about)
        mbar.add_cascade(label="Help", menu=m_help)
        self.config(menu=mbar)

    def clear_view(self):
        if self.view is not None:
            self.view.destroy()
            self.view = None

    def show_home(self):
        self.clear_view()
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.view = frame

        tk.Label(frame, text="AI & Data Science Quiz", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(frame, text="Choose a category and start a timed quiz.", font=("Arial", 12)).pack(pady=5)

        sel = tk.Frame(frame)
        sel.pack(pady=10)
        tk.Label(sel, text="Category:", font=("Arial", 12)).grid(row=0, column=0, padx=6, pady=6, sticky="e")
        cat_combo = ttk.Combobox(sel, values=list(CATEGORIES.keys()), textvariable=self.category_var, state="readonly", width=25)
        cat_combo.grid(row=0, column=1, padx=6, pady=6)

        tk.Button(frame, text="Start Quiz", width=18, command=self.start_quiz).pack(pady=10)

        # Stats placeholder
        self.last_summary_lbl = tk.Label(frame, text="", font=("Arial", 11))
        self.last_summary_lbl.pack(pady=5)

        # Footer
        tk.Label(frame, text="Free, offline, educational demo. Create/extend your own JSON question banks.", fg="#555").pack(side="bottom", pady=10)

    def start_quiz(self):
        cat = self.category_var.get()
        questions = self.questions_by_category.get(cat, [])
        if not questions:
            messagebox.showinfo("No Questions", "This category has no questions loaded.")
            return
        self.engine = QuizEngine(questions, self.settings)
        self.show_quiz()

    def show_quiz(self):
        self.clear_view()
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=16, pady=12)
        self.view = frame

        header = tk.Frame(frame)
        header.pack(fill="x")
        self.timer_lbl = tk.Label(header, text="Time: --", font=("Arial", 12, "bold"), fg="#aa0000")
        self.timer_lbl.pack(side="right")
        self.progress_lbl = tk.Label(header, text="Question 1", font=("Arial", 12))
        self.progress_lbl.pack(side="left")

        q_area = tk.LabelFrame(frame, text="Question")
        q_area.pack(fill="both", expand=True, pady=10)
        self.q_text = tk.Label(q_area, text="", wraplength=720, justify="left", font=("Arial", 12))
        self.q_text.pack(anchor="w", padx=10, pady=10)

        self.answer_area = tk.Frame(q_area)
        self.answer_area.pack(fill="x", padx=10, pady=10)

        nav = tk.Frame(frame)
        nav.pack(fill="x")
        self.submit_btn = tk.Button(nav, text="Submit", command=self.on_submit)
        self.submit_btn.pack(side="right", padx=6)
        self.skip_btn = tk.Button(nav, text="Skip", command=self.on_skip)
        self.skip_btn.pack(side="right", padx=6)

        self.render_question()
        self.tick_timer()

    def render_question(self):
        # Clear answers
        for child in self.answer_area.winfo_children():
            child.destroy()
        q = self.engine.current_question()
        if q is None:
            self.show_results()
            return
        idx = self.engine.index + 1
        total = len(self.engine.order)
        self.progress_lbl.config(text=f"Question {idx}/{total}")
        self.q_text.config(text=q["question"])

        self.user_var = None
        if q["type"] == "mcq":
            self.user_var = tk.StringVar(value="")
            for opt in q.get("options", []):
                ttk.Radiobutton(self.answer_area, text=opt, value=opt, variable=self.user_var).pack(anchor="w", pady=2)
        else:
            self.user_var = tk.StringVar()
            entry = ttk.Entry(self.answer_area, textvariable=self.user_var, width=60)
            entry.pack(anchor="w")
            entry.focus_set()
            ttk.Label(self.answer_area, text="Hint: Short answer, case-insensitive, accepts close matches").pack(anchor="w", pady=4)

    def tick_timer(self):
        if not self.engine or not self.engine.has_next():
            return
        left = self.engine.time_left()
        self.timer_lbl.config(text=f"Time: {left}s")
        if left <= 0:
            self.engine.forced_timeout()
            if self.engine.has_next():
                self.render_question()
                self.after(200, self.tick_timer)
            else:
                self.show_results()
            return
        self.after(250, self.tick_timer)

    def on_submit(self):
        q = self.engine.current_question()
        if q is None:
            return
        ans = ""
        if isinstance(self.user_var, tk.StringVar):
            ans = self.user_var.get()
        if q["type"] == "mcq" and not ans:
            messagebox.showinfo("Answer Required", "Please select an option or Skip.")
            return
        self.engine.submit_answer(ans)
        if self.engine.has_next():
            self.render_question()
        else:
            self.show_results()

    def on_skip(self):
        self.engine.submit_answer("")
        if self.engine.has_next():
            self.render_question()
        else:
            self.show_results()

    def show_results(self):
        self.clear_view()
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=16, pady=12)
        self.view = frame

        summary = self.engine.summary()
        tk.Label(frame, text="Quiz Results", font=("Arial", 18, "bold")).pack(pady=6)
        tk.Label(frame, text=f"Score: {summary['correct']} / {summary['total']}").pack()
        tk.Label(frame, text=f"Accuracy: {summary['accuracy']}%").pack()
        tk.Label(frame, text=f"Time: {summary['elapsed_sec']} sec").pack(pady=4)

        # Review table
        cols = ("#", "Question", "Your Answer", "Correct", "Result", "Time(s)")
        tree = ttk.Treeview(frame, columns=cols, show="headings", height=10)
        for c in cols:
            tree.heading(c, text=c)
            width = 50 if c in ("#", "Time(s)") else (90 if c == "Result" else 220)
            tree.column(c, width=width, anchor="center" if c in ("#", "Result", "Time(s)") else "w")
        tree.pack(fill="both", expand=True, pady=10)

        for i, a in enumerate(self.engine.answers, 1):
            user_show = a["user_answer"] if a["user_answer"] else "(blank)"
            res = "✓" if a["is_correct"] else "✗"
            tree.insert("", "end", values=(i, a["question"], user_show, a["correct_answer"], res, a["time_taken_sec"]))

        # Explanation panel
        exp_frame = tk.LabelFrame(frame, text="Explanation")
        exp_frame.pack(fill="x", pady=6)
        self.exp_text = tk.Text(exp_frame, height=4, wrap="word")
        self.exp_text.pack(fill="x", padx=6, pady=6)
        self.exp_text.insert("end", "Select a row to view explanation.")
        self.exp_text.config(state="disabled")

        def on_select(event):
            sel = tree.selection()
            if not sel:
                return
            idx = tree.index(sel[0])
            exp = self.engine.answers[idx].get("explanation", "")
            self.exp_text.config(state="normal")
            self.exp_text.delete("1.0", "end")
            self.exp_text.insert("end", exp if exp else "No explanation provided.")
            self.exp_text.config(state="disabled")
        tree.bind("<<TreeviewSelect>>", on_select)

        # Actions
        actions = tk.Frame(frame)
        actions.pack(fill="x", pady=6)
        ttk.Button(actions, text="Save Session", command=self.export_session).pack(side="left", padx=4)
        ttk.Button(actions, text="New Quiz", command=self.show_home).pack(side="right", padx=4)

        # Update home summary text
        self.last_summary_lbl = None  # will be recreated on home

    def export_session(self):
        if not self.engine:
            # Allow exporting question template too
            pass
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        payload = {
            "app": APP_TITLE,
            "settings": self.settings,
            "summary": self.engine.summary() if self.engine else {},
            "answers": self.engine.answers if self.engine else []
        }
        try:
            save_json(path, payload)
            messagebox.showinfo("Saved", f"Session exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def import_questions(self):
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            qs = load_questions(path)
            if not qs:
                messagebox.showwarning("Import", "No questions found in file.")
                return
            # Ask user where to place
            top = tk.Toplevel(self)
            top.title("Add to Category")
            tk.Label(top, text="Select target category:").pack(padx=10, pady=8)
            cat_var = tk.StringVar(value=list(CATEGORIES.keys())[0])
            combo = ttk.Combobox(top, values=list(CATEGORIES.keys()), textvariable=cat_var, state="readonly")
            combo.pack(padx=10, pady=8)
            def do_add():
                cat = cat_var.get()
                self.questions_by_category.setdefault(cat, []).extend(qs)
                # Also persist back to file for that category
                save_path = CATEGORIES.get(cat)
                if save_path:
                    existing = []
                    if os.path.exists(save_path):
                        existing = load_questions(save_path)
                    existing.extend(qs)
                    save_json(save_path, existing)
                messagebox.showinfo("Imported", f"Added {len(qs)} question(s) to {cat}.")
                top.destroy()
            ttk.Button(top, text="Add", command=do_add).pack(pady=8)
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import: {e}")

    def show_settings(self):
        top = tk.Toplevel(self)
        top.title("Quiz Settings")
        top.transient(self)
        top.grab_set()

        sv_time = tk.StringVar(value=str(self.settings.get("time_per_question_sec", 30)))
        sv_num = tk.StringVar(value=str(self.settings.get("num_questions", 5)))
        sv_shuffle = tk.BooleanVar(value=self.settings.get("shuffle", True))

        form = tk.Frame(top)
        form.pack(padx=10, pady=10)

        ttk.Label(form, text="Time per question (sec):").grid(row=0, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(form, textvariable=sv_time, width=10).grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(form, text="Number of questions:").grid(row=1, column=0, padx=6, pady=6, sticky="e")
        ttk.Entry(form, textvariable=sv_num, width=10).grid(row=1, column=1, padx=6, pady=6)

        ttk.Checkbutton(form, text="Shuffle questions", variable=sv_shuffle).grid(row=2, column=0, columnspan=2, padx=6, pady=6, sticky="w")

        def apply_settings():
            try:
                t = int(sv_time.get())
                n = int(sv_num.get())
                if t <= 0 or n <= 0:
                    raise ValueError
                self.settings["time_per_question_sec"] = t
                self.settings["num_questions"] = n
                self.settings["shuffle"] = bool(sv_shuffle.get())
                messagebox.showinfo("Settings", "Settings updated.")
                top.destroy()
            except Exception:
                messagebox.showwarning("Invalid", "Enter positive integers for time and number.")
        ttk.Button(top, text="Save", command=apply_settings).pack(pady=6)

    def show_about(self):
        messagebox.showinfo("About", f"{APP_TITLE}\nFree, offline Tkinter quiz for AI & Data Science.\nCreate your own JSON question banks.")

    def on_close(self):
        self.destroy()

if __name__ == "__main__":
    # Ensure data dirs exist
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(ASSETS_DIR, exist_ok=True)
    app = QuizApp()
    app.mainloop()
