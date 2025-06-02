import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class TelaBase(ttk.Frame):
    def __init__(self, container, title=None):
        super().__init__(container)

        img_path = os.path.join(os.path.dirname(__file__), '..', 'img', 'graal.jpg')
        try:
            img = Image.open(img_path)
            try:
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                resample = Image.LANCZOS
            img = img.resize((38, 38), resample)
            self.icon_img = ImageTk.PhotoImage(img)
            icon_label = tk.Label(self, image=self.icon_img, bg='#23272b')
            icon_label.grid(row=0, column=0, padx=(10, 10), pady=10, sticky="w")
            col_offset = 1
        except Exception:
            col_offset = 0
        if title:
            label = ttk.Label(self, text=title, font=("Arial", 16, "bold"))
            label.grid(row=0, column=col_offset, columnspan=2, pady=10, sticky="w")
