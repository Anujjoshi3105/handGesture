import pickle
import numpy as np
import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from resources.utils import hand_gesture

class PredictApp:
    def __init__(self, root):
        self.root = root
        self.capturing = False
        self.capture = None
        self.model_name = ""
        self.create_gui()

    def create_gui(self):
        self.canvas = tk.Canvas(self.root, width=640, height=480)
        self.canvas.pack(side='left', padx=20, pady=10)

        menu_panel = ttk.Frame(self.root)
        menu_panel.pack(side='left', fill='both', expand=True, pady=50)

        row1_frame = ttk.Frame(menu_panel)
        row1_frame.pack(pady=50)

        self.sign_label = ttk.Label(row1_frame, text="Result: Blank", font='comicsans 18 bold')
        self.sign_label.pack(side=tk.LEFT, padx=10)

        self.model_label = ttk.Label(menu_panel, text=self.model_name)
        self.model_label.pack()
        browse_button = ttk.Button(menu_panel, text="Model", command=self.browse_file)
        browse_button.pack(pady=5)

        row3_frame = ttk.Frame(menu_panel)
        row3_frame.pack(pady=10)

        self.capture_button = ttk.Button(row3_frame, text=" Start ", command=self.toggle_capture)
        self.capture_button.pack(side=tk.LEFT, pady=70)

        self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW)

        self.root.after(10, self.capture_frames)

    def toggle_capture(self):
        if not self.model_name:
            messagebox.showinfo('WARNING', 'MODEL is not selected')
            return

        self.capturing = not self.capturing
        self.capture_button['text'] = ' Stop ' if self.capturing else ' Start '

        if self.capturing:
            self.capture = cv2.VideoCapture(0)
        else:
            if self.capture is not None:
                self.capture.release()
                self.capture = None

    def capture_frames(self):
        if self.capturing and self.capture is not None:
            ret, frame = self.capture.read() 

            if ret:
                frame = cv2.flip(frame, 1)
                try:
                    with open(self.model_name, 'rb') as f:
                        model_dict = pickle.load(f)
                except:
                    messagebox.showinfo('WARNING', 'MODEL is not trained!')
                    return
                
                model = model_dict['model']
                data = hand_gesture(frame)
                
                try:
                    prediction = model.predict([np.asarray(data)])
                except:
                    prediction = ["blank"]
                self.sign_label['text'] = f'Result: {prediction[0].upper()}'

                self.update_frame_preview(frame)
        else:
            self.display_default_image()

        self.root.after(10, self.capture_frames)

    def update_frame_preview(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.canvas.itemconfig(self.image_id, image=photo)
        self.canvas.image = photo

    def display_default_image(self):
        logo = tk.PhotoImage(file='resources/images/handsign.png')
        self.canvas.itemconfig(self.image_id, image=logo)
        self.canvas.image = logo

    def browse_file(self):
        modelfile = filedialog.askopenfilename(filetypes=[("models", ('*.p',))])
        if modelfile:
            self.model_name = modelfile
            self.model_label.config(text=self.model_name)

if __name__ == "__main__":
    root = tk.Tk()
    app = PredictApp(root)
    root.mainloop()