#This script will generate the boilerplate files (HTML, CSS, Python) based on what c7_engine decides
import os

def generate_project(project_details, base_path="generated_projects/"):
    name = project_details.get("type", "unnamed")
    path = os.path.join(base_path, name.replace(" ", "_"))

    os.makedirs(path, exist_ok=True)

    with open(os.path.join(path, "README.md"), "w") as f:
        f.write(f"# {name.capitalize()}\n\Generated by Create7.")

    if "web_app" in project_details["type"]:
        with open(os.path.join(path, "app.py"), "w") as f:
            f.write("from flask import Flask, render_template\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello from Create7!'")
    return path