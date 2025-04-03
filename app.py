from flask import Flask, render_template, request

app = Flask(__name__)

history = []

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        input_data = request.form["input"]
        mode = request.form["mode"]

        try:
            if mode == "dec_to_bin":
                result = bin(int(input_data))[2:]
            elif mode == "bin_to_dec":
                result = str(int(input_data, 2))
            elif mode == "text_to_bin":
                result = ' '.join(format(ord(c), '08b') for c in input_data)
            elif mode == "bin_to_text":
                result = ''.join(chr(int(b, 2)) for b in input_data.split())
            history.append(f"{input_data} -> {result}")
        except:
            result = "Invalid input!"

    return render_template("index.html", result=result, history=history[-5:])

#only used locally - not in production
if __name__ == "__main__":
    app.run()
