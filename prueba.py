import tkinter as tk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My App")
        self.config(width=300, height=200)
        self.entry_display=tk.Entry(self, width=50)
        self.entry_display.place(x=10, y=10)
        self.entry_display.place(x=30, y=10)
        