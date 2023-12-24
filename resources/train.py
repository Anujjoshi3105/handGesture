import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import threading
from resources.utils import *

class TrainApp:
    def __init__(self, root):
        self.root = root
        self.directory = os.getcwd()
        self.create_gui()

    def create_gui(self):
        images_frame = ttk.Frame(self.root)
        images_frame.pack(side='left')

        file_frame = ttk.Frame(images_frame)
        file_frame.pack(side='left', pady=5)
        file_frame1 = ttk.Frame(images_frame)
        file_frame1.pack(side='left', pady=5, padx=10)

        # Create Y-scrollbar
        listbox_yscrollbar = tk.Scrollbar(file_frame)
        listbox_yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create X-scrollbar
        listbox_xscrollbar = tk.Scrollbar(file_frame, orient=tk.HORIZONTAL)
        listbox_xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Create Listbox with both Y and X-scrollbars
        self.file_listbox = tk.Listbox(file_frame, selectmode=tk.MULTIPLE, yscrollcommand=listbox_yscrollbar.set, xscrollcommand=listbox_xscrollbar.set, width=60, height=30)
        self.file_listbox.pack(expand=True, fill="both")

        # Configure both Y and X-scrollbars
        listbox_yscrollbar.config(command=self.file_listbox.yview)
        listbox_xscrollbar.config(command=self.file_listbox.xview)
        button_frame = ttk.Frame()
        button_frame.pack(side='left')

        add_button = ttk.Button(file_frame1, text="Add File(s)", command=self.add_file)
        self.remove_button = ttk.Button(file_frame1, text="Remove File(s)", command=self.remove_selected)
        self.clear_button = ttk.Button(file_frame1, text="Clear List", command=self.clear_list)
        add_button.pack(side='top', pady=5)
        self.remove_button.pack(side='top', pady=5)
        self.clear_button.pack(side='top', pady=5)

        self.train_frame = ttk.Frame(self.root)
        self.train_frame.pack(pady=80)

        self.model_name = ttk.Frame(self.train_frame)
        self.model_name.pack(side='top')

        self.filename_label = ttk.Label(self.model_name, text="Enter model name:")
        self.filename_label.pack(side='left', padx=5, pady=5)
        self.file_name = tk.StringVar()
        self.filename_entry = ttk.Entry(self.model_name, textvariable=self.file_name, width=30)
        self.filename_entry.pack(side='left', padx= 5, pady=5)

        self.folder_frame = ttk.Frame(self.train_frame)
        self.folder_frame.pack(side='top', pady=30)

        self.folder_label = ttk.Label(self.folder_frame, text=self.directory)
        self.folder_label.pack(side='top', pady= 5)
        self.browse_folder_button = ttk.Button(self.folder_frame, text="Location", command=self.browse_folder)
        self.browse_folder_button.pack(side='top', pady= 5)

        self.start_button = ttk.Button(self.train_frame, text="Start", command=self.check_images)
        self.start_button.pack(pady=30)

        self.model_label = ttk.Label(self.train_frame, text='No Model is trained', font='18')
        self.model_label.pack(pady=20)

        self.progress = ttk.Progressbar(self.train_frame, orient='horizontal', length=300, mode="indeterminate")
        self.progress.pack()

        ttk.Label(self.root, text='NOTE: Dataset should be in format {sign}_{xx}.jpg', font='comicsans 10 bold').pack(padx=20, pady=10)

    def add_file(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("images", ('*.jpg', '*.jpeg', '*.png'))])
        for file_path in file_paths:
            self.file_listbox.insert(tk.END, file_path)

    def remove_selected(self):
        selected_indices = self.file_listbox.curselection()
        for i in selected_indices[::-1]:
            self.file_listbox.delete(i)

    def clear_list(self):
        self.file_listbox.delete(0, tk.END)

    def browse_folder(self):
        selected_folder = filedialog.askdirectory()
        if selected_folder:
            self.folder_label.config(text=selected_folder)
            self.directory = selected_folder
    def check_images(self):
        if self.file_name.get() == '':
            messagebox.showinfo('Missing', 'File Name is missing!')
            return
        
        all_items = range(self.file_listbox.size())
        selected_items = self.file_listbox.curselection()
        self.imgList = [self.file_listbox.get(i) for i in all_items if i not in selected_items]

        if not self.imgList:
            messagebox.showinfo('Missing', 'Dataset is missing!')
            return

        self.start_button['text'] = 'Processing'
        self.start_button['state'] = 'disabled'
        self.model_label['text'] = 'Training the model, please wait...'

        # Start training in a separate thread
        training_thread = threading.Thread(target=self.selected_images)
        training_thread.start()

    def selected_images(self):
        # Start the progress bar
        self.progress.start()

        process_data(self.imgList, self.directory, self.file_name.get())
        score = train_model(self.directory, self.file_name.get())

        # Stop the progress bar
        self.progress.stop()

        # Update the GUI when training is done
        self.root.after(0, self.update_model_label, score)  # Pass your actual accuracy here

    def update_model_label(self, score):
        self.model_label.config(text=f'Accuracy of the model is : {score}%')
        self.start_button['text'] = 'Start'
        self.start_button['state'] = 'normal'

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainApp(root)
    root.mainloop()