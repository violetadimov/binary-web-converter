from app import users, projects

def get_user_by_id(user_id):
    return users.find_one({"_id": user_id})

def save_project(data):
    return projects.insert_one(data)