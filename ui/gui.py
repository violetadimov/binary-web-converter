import tkinter as tk
from tkinter import ttk

from app import history
from utils import binary_tools

class BinaryConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Converter - Desktop")
        self.root.geometry("600x600")
        self.build_ui()
        self.history_file = "history_file/conversion_history.txt"
        self.history = []

    def build_ui(self):
        self.mode = tk.StringVar(value="Decimal to Binary")
        modes = [
            ("Text to Binary", "text_to_bin"),
            ("Binary to Text", "bin_to_text"),
            ("Decimal to Binary", "dec_to_bin"),
            ("Binary to Decimal", "bin_to_dec"),
            # ("Decimal to Text", "dec_to_text"),
            # ("Text to Decimal", "text_to_dec"),
        ]

        tk.Label(self.root, text="Select Mode:").pack()
        ttk.Combobox(self.root, textvariable=self.mode, values=[m[0] for m in modes]).pack(pady=5)

        self.dark_mode = tk.BooleanVar()
        toggle = ttk.Checkbutton(self.root, text="Dark Mode", variable=self.dark_mode, command=self.toggle_theme)
        toggle.pack(pady=5)

        tk.Label(self.root, text="Enter a text or number:").pack()
        self.input = tk.Text(self.root, height=5, width=60)
        self.input.pack()

        tk.Button(self.root, text="Converter", command=self.convert).pack(pady=10)

        tk.Label(self.root, text="Answer:").pack()
        self.output = tk.Text(self.root, height=5, width=60, state=tk.DISABLED)
        self.output.pack()

        tk.Label(self.root, text="History( Last 5):").pack()
        self.history_box = tk.Text(self.root, height=5, width=60, state=tk.DISABLED)
        self.history_box.pack()

        #buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Clear History", command=self.clear_history).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Open File", command=self.open_history_file).pack(side=tk.RIGHT, padx=10)

    def convert(self):
        mode = self.mode.get()
        mode_map = {
            "Text to Binary": "text_to_bin",
            "Binary to Text": "bin_to_text",
            "Decimal to Binary": "dec_to_bin",
            "Binary to Decimal": "bin_to_dec",
            # ("Decimal to Text", "dec_to_text"),
            # ("Text to Decimal", "text_to_dec"),
        }
        internal_mode = mode_map.get(mode)

        input_data = self.input.get("1.0", tk.END).strip()

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

        #save to history file
        with open(self.history_file, "w") as file:
            file.write(f"{internal_mode}: {input_data} -> {result}\n")

        # update in memory history list
        self.history.append(f"{internal_mode}: {input_data} -> {result}")
        self.history = self.history[-5:] # keeps only the last 5
        self.update_history_display()

        #display output
        self.output.config(state='normal')
        self.output.delete("1.0", tk.END)
        self.output.insert("1.0", result)
        self.output.config(state='disabled')

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
        import os
        os.system(f"open {self.history_file}")

    def toggle_theme(self):
        if self.dark_mode.get():
            self.root.configure(background="#2e2e2e")
            for widget in self.root.winfo_children():
                try:
                    widget.configure(background="#2e2e2e", foreground="white")
                except:
                    pass
        else:
            self.root.configure(background="SystemButtonFace")
            for widget in self.root.winfo_children():
                try:
                    widget.configure(background="SystemButtonFace", foreground="black")
                except:
                    pass