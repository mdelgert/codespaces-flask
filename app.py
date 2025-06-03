from flask import Flask, render_template, request
from gremlins.clean import clean_text

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world():
    cleaned = None
    input_text = ""
    if request.method == "POST":
        input_text = request.form.get("input_text", "")
        cleaned = clean_text(input_text)
    return render_template("index.html", title="Hello", cleaned=cleaned, input_text=input_text)
