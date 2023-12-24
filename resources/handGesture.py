import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk
import subprocess
from resources.collect import CollectApp
from resources.train import TrainApp
from resources.predict import PredictApp

class HandGestureApp:
    def __init__(self, root):
        self.root = root
        self.create_gui()
        
        heading = ttk.Frame(self.main_frame)
        heading.pack(side='top', fill='y', pady=10)

        logo = tk.PhotoImage(file='resources/images/logo.png')

        ttk.Label(heading, image=logo).pack(side='left')
        ttk.Label(heading, text='Hand Gesture', font='comicsans 32 bold').pack(side='left', padx=15)
        self.root.mainloop()

    def create_gui(self):
        self.root.title("Hand Gesture")
        self.root.iconbitmap('resources/images/favicon.ico')
        self.root.geometry('1100x750')
        self.root.resizable(width=False, height=False)
        
        self.style = ThemedStyle(self.root)
        self.style.set_theme("adapta")
        
        self.create_menu()
        self.create_mainframe()
        
    def create_mainframe(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True)
        self.collect_tab, self.train_tab, self.predict_tab, self.main_notebook = self.create_notebook()
        self.collect_frame = CollectApp(self.collect_tab)
        self.train_frame = TrainApp(self.train_tab)
        self.predict_frame = PredictApp(self.predict_tab)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_menu)
        
        themes_menu = tk.Menu(file_menu, tearoff=0)
        available_themes = sorted(theme.capitalize() for theme in self.style.get_themes())
        for theme in available_themes:
            themes_menu.add_command(label=theme, command=lambda theme=theme: self.switch_theme(theme))
        file_menu.add_cascade(label="Themes", menu=themes_menu)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation")
        help_menu.add_command(label="About us")

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.root.config(menu=menubar)

    def new_menu(self):
        subprocess.Popen(["python", 'main.py'])

    def switch_theme(self, theme_name):
        self.style.set_theme(theme_name.lower())

    def create_notebook(self):
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(side='bottom', padx=10, fill="x", expand=True)

        collect_tab = self.create_tab(notebook, "Collect")
        train_tab = self.create_tab(notebook, "Train")
        predict_tab = self.create_tab(notebook, "Predict")
        return collect_tab, train_tab, predict_tab, notebook

    def create_tab(self, notebook, tab_name):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=f'  {tab_name}  ')
        return tab

if __name__ == "__main__":
    root = tk.Tk()
    app = HandGestureApp(root)
    root.mainloop()