import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timezone
from pymongo import MongoClient
from bson.objectid import ObjectId
from c7_engine import interpret_command
from functools import wraps
#import os
from dotenv import load_dotenv
load_dotenv()
from auth import hash_password, check_password, get_user_by_email_or_username, create_user, is_premium_user


app = Flask(__name__)
app.secret_key = "super-secret-key"

# MongoDB Setup
client = MongoClient(os.environ["MONGO_URI"])
db = client["create7"]
users = db["users"]
projects = db["projects"]


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
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/create", methods=["GET", "POST"])
@login_required
def create7():
    user_id = session["user"]["id"]
    user = users.find_one({"_id": ObjectId(user_id)})

    if request.method == "POST":
        if not is_premium_user(user):
            return redirect("/premium-required")

        description = request.form["description"]
        output = interpret_command(description)

        projects.insert_one({
            "user_id": ObjectId(user_id),
            "description": description,
            "code": output,
            "timestamp": datetime.now(timezone.utc)
        })

        return render_template("create7.html", output=output, description=description)

    return render_template("create7.html")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    project_list = projects.find({"user_id": ObjectId(user_id)}).sort("timestamp", -1)
    return render_template("history.html", projects=project_list)


@app.route("/premium")
@login_required
def premium():
    return render_template("premium.html")


@app.route("/premium-required")
@login_required
def premium_required():
    return render_template("premium_required.html")

@app.route("/my-projects", methods=["GET"])
def my_projects():
    return render_template("my_projects.html")
# ----- Development Server -----
if __name__ == "__main__":
    app.run(debug=True)


