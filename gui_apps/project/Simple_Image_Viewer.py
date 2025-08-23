import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # pip install pillow

img_tk = None

def open_image():
    global img_tk
    path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if not path:
        return
    try:
        img = Image.open(path)
        img.thumbnail((500, 400))
        img_tk = ImageTk.PhotoImage(img)
        lbl.config(image=img_tk, text="")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Image Viewer")

tk.Button(root, text="Open Image", command=open_image).pack(pady=10)
lbl = tk.Label(root, text="No image loaded", width=60, height=20, bg="#eee")
lbl.pack(padx=10, pady=10)

root.mainloop()
