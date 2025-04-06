
from flask import Flask, render_template, request
from utils import binary_tools
import  os
from pymongo import MongoClient

#clear the conversion history each  time the app starts
with open("history_file/conversion_history.txt", "w") as file:
    file.write("")

#Flask App Setup
template_dir = os.path.abspath("templates")
#I
app = Flask(__name__, template_folder=template_dir)

#MongoDB Setup
MONGO_URI = "mongodb+srv://binaryUser:G@W93@converter.ghsrsp2.mongodb.net/?retryWrites=true&w=majority&appName=Converter"
client = MongoClient(MONGO_URI)
db = client['converter']
history_collection = db['conversion_history']

#history = []

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

            else: result = "Invalid mode"

            #Save MongoDB
            history_collection.insert_one({
                "input": input_data,
                "mode": mode,
                "result": result
            })

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result) #history=history[-5:])

@app.route("/history", methods=["GET"])
def view_history():
    #with open("history_file/conversion_history.txt", "r") as f:
    #get the last 10 conversion, newest first.
    history = list(history_collection.find().sort("_id", -1).limit(10))
    return render_template("history.html", history=history)

@app.route("/clear-history", methods=["POST"])
def clear_history():
    history_collection.delete_many({})
    return render_template("history.html", history=[])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

