import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timezone
from pymongo import MongoClient
from bson.objectid import ObjectId
from c7_engine import interpret_command
from functools import wraps
from utils.db import client, db, users, projects
from dotenv import load_dotenv
load_dotenv()
from auth import hash_password, check_password, get_user_by_email_or_username, create_user, is_premium_user


app = Flask(__name__)
app.secret_key = "super-secret-key"



# ----- Auth Decorators -----
def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return wrapped


# ----- Routes -----
@app.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]

        if password != confirm:
            return render_template("signup.html", error="Passwords do not match.")

        if get_user_by_email_or_username(email) or get_user_by_email_or_username(username):
            return render_template("signup.html", error="User already exists.")

        hashed = hash_password(password)
        user_id = create_user(email, username, hashed)
        session["user_id"] = str(user_id)
        return redirect("/dashboard")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_input = request.form["user_input"]
        password = request.form["password"]

        user = get_user_by_email_or_username(user_input)
        if user and check_password(password, user["password"]):
            session["user_id"] = str(user["_id"])
            return redirect("/dashboard")
        return render_template("login.html", error="Invalid credentials.")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/dashboard")
#@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/create", methods=["GET", "POST"])
#@login_required
def create7():
    #temporary bypass for development (commented out session for now)
    #user_id = session["user"]["id"]
    #user = users.find_one({"_id": ObjectId(user_id)})
    user_id = "dev_user" #placeholder
    user = {"_id": "dev_user", "premium": True} #mock user

    if request.method == "POST":
        if not user.get("premium"): #is_premium_user(user)
            return redirect("/premium-required")

        description = request.form["description"]
        output = interpret_command(description)

        projects.insert_one({
            "user_id": user_id, #ObjectId(user_id)
            "description": description,
            "code": output,
            "timestamp": datetime.now(timezone.utc)
        })

        return render_template("create7.html", output=output, description=description)

    return render_template("create7.html")


@app.route("/history")
#@login_required
def history():
    #Tempory mock user for development
    #user_id = session["user_id"]
    user_id = "dev_user"
    #project_list = projects.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1)
    project_cursor = projects.find({"user_id": user_id}).sort("timestamp", -1)
    project_list = list(project_cursor)
    return render_template("history.html", projects=project_list)


@app.route("/premium")
#@login_required
def premium():
    return render_template("premium.html")


@app.route("/premium-required")
#@login_required
def premium_required():
    return render_template("premium_required.html")

@app.route("/my-projects", methods=["GET"])
def my_projects():
    return render_template("my_projects.html")

@app.route("/save_project", methods=["POST"])
def save_project():
    data = request.get_json()
    user_id = session.get("user_id") or "guest"

    project = {
        "user_id": user_id,
        "description": data.get("description", "Untitled"),
        "html": data.get("html", ""),
        "css": data.get("css", ""),
        "js": data.get("js", ""),
        "backend": data.get("backend", ""),
        "timestamp": datetime.utcnow()
    }

    db.projects.insert_one(project)
    return jsonify({"message": "Project saved successfully!"})

@app.route('/template')
def template():
    return render_template('template.html')

@app.route('/settings', methods=["GET", "POST"])
def settings():
    return render_template('settings.html')

@app.route('/help')
def help_page():
    return render_template('help.html')

# ----- Development Server -----
if __name__ == "__main__":
    app.run(debug=True)


