
from flask import Flask, render_template, request
from utils import binary_tools
import sys
import  os

template_dir = os.path.abspath("templates")

app = Flask(__name__, template_folder=template_dir)

history = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        input_data = request.form["input"]
        mode = request.form["mode"]

        try:
            if mode == "dec_to_bin":
                result = binary_tools.decimal_to_binary(input_data)
            elif mode == "bin_to_dec":
                result = binary_tools.binary_to_decimal(input_data)
            elif mode == "text_to_bin":
                result = binary_tools.text_to_binary(input_data)
            elif mode == "bin_to_text":
                result = binary_tools.binary_to_text(input_data)

        except:
            result = "Invalid input!"

    return render_template("index.html", result=result, history=history[-5:])

#only used locally - not in production
if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "web"

    if mode == "gui":
        import tkinter as tk
        from ui.gui import BinaryConverterGUI

        root = tk.Tk()
        app = BinaryConverterGUI(root)
        root.mainloop()

    else:
        from ui.web import run_web_app
        run_web_app()
        #app.run()
