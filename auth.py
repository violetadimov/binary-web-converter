from flask import Blueprint, request, redirect, session, url_for
import bcrypt
from utils.db import users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.form
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    confirm = data.get("confirm")

    if password != confirm:
        return "Passwords do not match"

    if users.find_one({"$or": [{"email": email}, {"username": username}]}):
        return "Email or username already exists"

    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    users.insert_one({
        "email": email,
        "username": username,
        "password": hashed_pw,
        "is_premium": False
    })
    return redirect(url_for("login_page"))

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.form
    identifier = data.get("identifier")
    password = data.get("password")

    user = users.find_one({
        "$or": [{"email": identifier}, {"username": identifier}]
    })

    if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        session["user"] = {
            "id": str(user["_id"]),
            "username": user["username"],
            "is_premium": user.get("is_premium", False)
        }
        return redirect("/dashboard")
    return "Invalid login"

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_pw):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw)

def get_user_by_email_or_username(identifier):
    return users.find_one({ "$or": [{"email": identifier}, {"username": identifier}] })

def create_user(email, username, password):
    hashed_pw = hash_password(password)
    users.insert_one({
        "email": email,
        "username": username,
        "password": hashed_pw,
        "is_premium": False
    })

def is_premium_user(user):
    return user.get("is_premium", False)


