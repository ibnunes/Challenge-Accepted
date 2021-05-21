from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        return "<p>Login method POST!</p>"
    else:
        return "<p>Login method GET!</p>"