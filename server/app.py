import os
from flask import Flask, render_template

app = Flask(__name__)

# Serve React App
@app.route('/')
def my_index():
    return render_template("index.html", token = "HELLO")


app.run(debug=True)