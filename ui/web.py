from flask import Flask, render_template, request, redirect
from utils import binary_tools
import os
from datetime import datetime
import json

history_file = "history_file/conversion_history.txt"

#explicitly tell flask where template lives
template_dir = os.path.abspath("templates")
static_dir = os.path.abspath("static")

theme_path = "theme.json"
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)



@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    last_conversions = []

    if request.method == "POST":
        if "input" in request.form and "mode" in request.form:
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

            except Exception as e:
                result = f"Error: {str(e)}"

            #add timestamp and save to file
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #save to file
            with open(history_file, "a") as f:
                f.write(f"[{timestamp}] {mode}: {input_data} -> {result}\n")

    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            all_lines = f.readlines()
            if all_lines:
                last_conversions = [line.strip() for line in all_lines[-5:]]
            else:
                last_conversions = []


    return render_template("index.html", result=result, history=last_conversions)
@app.route("/clear", methods=["POST"])
def clear():
    open(history_file, "w").close()
    return redirect("/")

@app.route("/history", methods=["GET"])
def view_history():
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = [line.strip() for line in f.readlines()]
    return render_template("history.html", history=history)

@app.route("/get-theme", methods=["GET"])
def get_theme():
    if os.path.exists(theme_path):
        with open(theme_path, "r") as f:
            data = json.loads(f.read())
            return {"theme": data.get("theme", "light")}
    return {"theme": "light"}

@app.route("/set-theme", methods=["POST"])
def set_theme():
    new_theme = request.json.get("theme")
    with open(theme_path, "w") as f:
        json.dump({"theme": new_theme}, f)
    return {"message": "Theme updated."}

def run_web_app():
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=8080, debug=True)