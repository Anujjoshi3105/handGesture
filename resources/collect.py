import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os

class CollectApp:
    def __init__(self, root):
        self.root = root
        self.capturing = False
        self.capture = None
        self.frame_count = 0
        self.frame_name = ""
        self.save_folder = os.getcwd()

        self.create_gui()

    # Create the GUI elements    
    def create_gui(self):
        self.webcam = ttk.Frame(self.root)
        self.webcam.pack(side='left', fill='both', expand=True)
        self.menu_panel = ttk.Frame(self.root)
        self.menu_panel.pack(side='left', pady=70, padx=70, fill='both', expand=True)
        
        self.canvas = tk.Canvas(self.webcam, width=640, height=480)
        self.canvas.pack(side='left', padx=20)

        self.row1_frame = ttk.Frame(self.menu_panel)
        self.row1_frame.pack(side='top', fill='both', expand=True)

        self.frame_label = ttk.Label(self.row1_frame, text="Enter sign:")
        self.frame_label.pack(side='left', padx=10)
        self.name_entry = ttk.Entry(self.row1_frame, width=30)
        self.name_entry.pack(side='left')

        self.row2_frame = ttk.Frame(self.menu_panel)
        self.row2_frame.pack(side='top', pady=50, fill='both', expand=True)

        self.folder_label = ttk.Label(self.row2_frame, text=self.save_folder)
        self.folder_label.pack(side='top')
        self.browse_button = ttk.Button(self.row2_frame, text=" Location ", command=self.browse_folder)
        self.browse_button.pack(side='top', pady=10)

        self.row3_frame = ttk.Frame(self.menu_panel)
        self.row3_frame.pack(side='top', pady=50)

        self.capture_button = ttk.Button(self.row3_frame, text="Start", command=self.start_capture)
        self.capture_button.pack(side='top')

        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW)

        self.root.after(10, self.capture_frames)

    def start_capture(self):
        self.frame_name = self.name_entry.get()
        self.capturing = not self.capturing
        if self.frame_name == '':
            self.show_message('SIGN is MISSING')
            return
        if self.capturing:
            self.capture_button['text'] = ' Stop '
            self.capture = cv2.VideoCapture(0)
        else:
            self.capture_button['text'] = ' Start '
            if self.capture is not None:
                self.capture.release()
                self.capture = None

    def capture_frames(self):
        if self.capturing and self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.flip(frame, 1)
                cv2.imwrite(self.generate_filename(), frame)
                self.frame_count += 1
                self.update_frame_preview(frame)
        else:
            # If not capturing, show an IMAGE
            logo = tk.PhotoImage(file='resources/images/handsign.png')
            self.canvas.itemconfig(self.image_id, image=logo)
            self.canvas.image = logo

        self.root.after(10, self.capture_frames)

    def generate_filename(self):
        filename = f"{self.frame_name}_{self.frame_count}.jpg"
        self.frame_count = 0
        while os.path.exists(os.path.join(self.save_folder, filename)):
            self.frame_count += 1
            filename = f"{self.frame_name}_{self.frame_count}.jpg"
        return os.path.join(self.save_folder, filename.upper())

    def update_frame_preview(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.canvas.itemconfig(self.image_id, image=photo)
        self.canvas.image = photo

    def browse_folder(self):
        folder_name = filedialog.askdirectory()
        if folder_name != '':
            self.save_folder = folder_name
            self.folder_label.config(text=self.save_folder)

    def show_message(self, message):
        messagebox.showinfo('MISSING', message)

if __name__ == "__main__":
    root = tk.Tk()
    app = CollectApp(root)
    root.mainloop()