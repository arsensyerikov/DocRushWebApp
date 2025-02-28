from flask import Flask, render_template, request
import random
import os

app = Flask(__name__, template_folder="//Users//arsensyerikov//Desktop//Leson//templates")

@app.route("/")
def index():
    random_number = random.randint(1, 100)

    return render_template("index.html", random_number=random_number)
    
if __name__ == "__main__":
    app.run(debug=True)