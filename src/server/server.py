from flask import Flask
from flask import request
import json

from .dbhelper.dbcontrol import *

app = Flask(__name__)

db = DBControl()
db.start()

@app.route("/login", methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        (ok, user_id) = db.loginUser(username, password)
        if ok:
            return json.dumps({ "success": { "user_id": user_id } })
        else:
            return json.dumps({ "error": "Unknown Error" })
    except (UsernameNotFound, WrongPassword) as ex:
        return json.dumps({ "error": ex.message })