import tkinter as tk
from tkinter import ttk

class TelaBase(ttk.Frame):
    def __init__(self, container, title=None):
        super().__init__(container)
        
        if title:
            label = ttk.Label(self, text=title, font=("Arial", 16, "bold"))
            label.grid(row=0, column=0, columnspan=2, pady=10)
