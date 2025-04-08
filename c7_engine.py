#c7_engine.py this will be the heart of Create7. it parses natural language, generates a plan and converts it into code
from pyexpat import features


def interpret_command(command):
    #basic natural language interpretation( to be expanded)
    if "todo app" in command.lower():
        return {
            "type": "web_app",
            "features": ["add task", "complete task", "delete task"],
            "tech_stack": ["HTML", "CSS", "JavaScript", "Flask"]
        }
    elif "blog" in command.lower():
        return {
            "type": "web_app",
            "features": ["create post", "edit post", "view post"],
            "tech_stack": ["Flask", "Jinja", "SQLite"]
        }
    return {"error": "Sorry, I couldn't understand your request yet."}