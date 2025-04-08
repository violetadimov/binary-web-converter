import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from datetime import datetime
#import subprocess

# Fix import for local script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import binary_tools

#MongoDB Setup
MONGO_URI = "mongodb+srv://binaryUser:G%40W93@converter.ghsrsp2.mongodb.net/?retryWrites=true&w=majority&appName=Converter"

#Mode display mapping
mode_display = {
            "dec_to_bin": "Decimal to Binary",
            "bin_to_dec": "Binary to Decimal",
            "text_to_bin": "Text to Binary",
            "bin_to_text": "Binary to Text",
        }

class BinaryConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Converter - Desktop")

        self.history_file = "history_file/conversion_history.txt"
        self.history = []

        #Mongo setup
        self.mongo_client = MongoClient(MONGO_URI)
        self.mongo_db = self.mongo_client['converter']
        self.mongo_collection = self.mongo_db['conversion_history']

        # Use cloud sync toggle, Variables
        self.mode = tk.StringVar(value="Text to Binary")
        self.use_cloud = tk.BooleanVar()
        self.dark_mode = tk.BooleanVar()

        #layout
        self.build_ui()

        self.use_cloud.set(False)  # start with local history by default

        #URI elements, dropdown mode selector
        #self.mode = tk.StringVar()
        #self.mode.set(mode_display["text_to_bin"])

    def build_ui(self):
        # input label and box
        tk.Label(root, text="Enter a text or number:").pack(anchor="w", padx=10)
        self.input = tk.Text(self.root, height=2, width=70)
        self.input.insert("1.0", " ")
        self.input.pack(padx=10, pady=(0, 10))

        #Conversion controls section with border
        conversion_frame = tk.LabelFrame(self.root, text="Conversion Controls", padx=10, pady=10)
        conversion_frame.pack(pady=10)

        # Row for columns, grid with 2 columns
        #row_frame = tk.Frame(conversion_frame)
        #row_frame.pack()

        # Column 1
        left_col = tk.Frame(conversion_frame)
        left_col.grid(row=0, column=0, padx=10)

        # Column 2
        right_col = tk.Frame(conversion_frame)
        right_col.grid(row=0, column=1, padx=10)

        #Left Column: dropdown and convert
        tk.Label(left_col, text="Conversion Mode:").pack(anchor="w")
        self.dropdown = ttk.Combobox(left_col, textvariable=self.mode, values=list(mode_display.values()), state="readonly")
        self.dropdown.pack(pady=2)

        ttk.Button(left_col, text="Convert", command=self.convert).pack(pady=2)

        #right column switch toggles
        ttk.Checkbutton(right_col, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme).pack(pady=2)
        ttk.Checkbutton(right_col, text="Use Cloud Sync", variable=self.use_cloud, command=self.refresh_history).pack(pady=2)

        #output box
        tk.Label(root, text="Result:").pack()
        self.output = tk.Text(self.root, height=2, width=60) # state=tk.DISABLED)
        self.output.pack(pady=(0, 10))

        #history box
        tk.Label(root, text="Conversion History:").pack()
        self.history_box = tk.Text(self.root, height=5, width=60,) # state=tk.DISABLED)
        self.history_box.pack()

        #buttons
        button_frame = tk.Frame(self.root, bg=self.root.cget("background"))
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Open File", command=self.open_history_file).pack(side=tk.LEFT, padx=10)

        self.load_history()
        self.update_history_display()


    def convert(self):
        mode_map = {v: k for k, v in mode_display.items()}
        internal_mode = mode_map.get(self.mode.get())
        input_data = self.input.get("1.0", tk.END).strip()

        #display_map = {v: k for k, v in mode_map.items()}
        #internal_mode = mode_map.get(mode)
        #input_data = self.input.get("1.0", tk.END).strip()

        #Perform Conversion
        if internal_mode == "text_to_bin":
            result = binary_tools.text_to_binary(input_data)
        elif internal_mode == "bin_to_text":
            result = binary_tools.binary_to_text(input_data)
        elif internal_mode == "dec_to_bin":
            result = binary_tools.decimal_to_binary(input_data)
        elif internal_mode == "bin_to_dec":
            result = binary_tools.binary_to_decimal(input_data)
        else:
            result = "[Error] Invalid mode"

        #Timestamp
        timestamp = datetime.now().strftime("%B %d - %I:%M %p")
        #display_mode = display_map.get(internal_mode, internal_mode)

        #save to history file or cloud
        if self.use_cloud.get():
            self.mongo_collection.insert_one({
                "timestamp": timestamp,
                "mode": self.mode.get(),
                "result": result,
                "input": input_data,
            })
        else:
            with open(self.history_file, "a") as file:
                file.write(f"{timestamp} - {self.mode.get()}: {input_data} -> {result}\n")


        self.load_history()
        self.update_history_display()

        #display output
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", result)
        self.output.config(state='disabled')

    def load_history(self):
        self.history.clear()

        if self.use_cloud.get():
            entries = self.mongo_collection.find().sort("_id", -1).limit(10)
            for entry in entries:
                self.history.append(f"{entry.get('timestamp')} - {entry.get('mode')}: {entry.get('input')} -> {entry.get('result')}")
        else:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r") as file:
                    lines = file.readlines()
                    self.history = [line.strip() for line in lines[-10:]]

    def update_history_display(self):
        self.history_box.config(state='normal')
        self.history_box.delete("1.0", tk.END)
        for line in self.history:
            self.history_box.insert(tk.END, line + "\n")
        self.history_box.config(state='disabled')

    def clear_history(self):
        self.history = []
        self.update_history_display()
        open(self.history_file, 'w').close()

    def open_history_file(self):
        #import os
        #os.system(f"open {self.history_file}")
        path = os.path.abspath(self.history_file)
        try:
            if sys.platform.startswith("darwin"):
                subprocess.run(["open", path])
            elif os.name == "nt":
                os.startfile(path)
            elif os.name == "posix":
                subprocess.run(["xdg-open", path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def refresh_history(self):
        self.load_history()
        self.update_history_display()

    def toggle_theme(self):
        bg, fg, boxbg = ("#2e2e2e", "white", "#444") if self.dark_mode.get() else ("SystemButtonFace", "black", "white")

        self.root.configure(background=bg)
        for widget in self.root.winfo_children():
                try:
                    widget.configure(background=bg, foreground=fg)
                    if isinstance(widget, tk.Text):
                        widget.configure(background=boxbg, foreground=fg, insertbackground=fg)
                except:
                    pass


    def on_close(self):
        self.mongo_client.close()
        self.root.destroy()

#Main Runner

if __name__ == "__main__":
    root = tk.Tk()
    app = BinaryConverterGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()