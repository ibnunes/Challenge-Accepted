from flask import Flask
from flask import request
import json

from dbhelper.dbcontrol import *
from utils.appauth import *

app = Flask(__name__)

db = DBControl()
appAuth = AppAuthenticationServer()
# db.start()

@app.route("/auth/hmac", methods=['GET'])
def getHMACKey():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    try:
        return json.dumps({"success" : db.getHMACKey()})
    except Exception as ex:
        return json.dumps({"error" : str(ex)})


@app.route("/auth/login", methods=['POST'])
def login():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
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


@app.route("/auth/signup", methods=['POST'])
def signup():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    ok = db.registerUser(username, password, email)
    if ok:
        return json.dumps({"success": True})
    else:
        return json.dumps({"error": "Unable to register user"})


@app.route("/auth/user", methods=['POST'])
def userExists():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    username = request.form['username']
    ok = db.userExists(username)
    return json.dumps({"success": ok})


@app.route("/auth/user", methods=['POST'])
def emailExists():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    email = request.form['email']
    ok = db.emailExists(email)
    return json.dumps({"success": ok})


@app.route("/user/email/", methods=['GET'])
def getEmail():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.args.get('id')
    email = db.getEmail(userid)
    if email is None:
        return json.dumps({"error": "Unable to fetch email"})
    else:
        return json.dumps({"success": email})


# Cypher Related Routes
@app.route("/challenge/cypher", methods=['GET'])
def getCypherChallenges():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    table = db.getAllCypherChallenges()
    if table is None:
        return json.dumps({"error": "Unable to fetch cypher challenges"})
    else:
        json_data=[]
        for result in table[1]:
            json_data.append(dict(zip(table[0],result)))
        return json.dumps({"success": json_data})


@app.route("/challenge/cypher/<chid>", methods=['GET'])
def getCypherChallenge(chid):
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    challenge = db.getCypherChallenge(chid)
    if challenge is None:
        return json.dumps({"error": "Unable to fetch cypher challenge"})
    else:        
        return json.dumps({"success": challenge})


@app.route("/challenge/cypher/lasttry", methods=['GET'])
def getCypherLastTry():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.args.get('userid')
    chid = request.args.get('chid')
    lastTry = db.getCypherLastTry(userid, chid)
    if lastTry is None:
        return json.dumps({"error": "Unable to fetch cypher last try"})
    else:
        return json.dumps({"success": lastTry})


@app.route("/challenge/cypher", methods=['POST'])
def addCypherChallenge():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.form["userid"]
    tip = request.form["tip"]
    msg = request.form["msg"]
    val = request.form["val"]
    iv  = request.form["iv"]
    hmac = request.form["hmac"]
    algo = request.form["algo"]
    ok = db.addCypherChallenge(userid, tip, msg, val, iv, hmac, algo)
    return json.dumps({"success": ok})


@app.route("/challenge/cypher/<chid>", methods=['PATCH'])
def updateCypherChallenge(chid):
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.form["userid"]
    date = request.form["date"]
    success = request.form["success"]
    ok = db.updateCypherChallengeTry(userid, chid, date, success)
    return json.dumps({"success": ok})


# Hash Related Routes
@app.route("/challenge/hash", methods=['GET'])
def getHashChallenges():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    table = db.getAllHashChallenges()
    if table is None:
        return json.dumps({"error": "Unable to fetch hash challenges"})
    else:
        json_data=[]
        for result in table[1]:
            json_data.append(dict(zip(table[0],result)))
        return json.dumps({"success": json_data})


@app.route("/challenge/hash/<chid>", methods=['GET'])
def getHashChallenge(chid):
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    challenge = db.getHashChallenge(chid)
    if challenge is None:
        return json.dumps({"error": "Unable to fetch cypher challenge"})
    else:        
        return json.dumps({"success": challenge})


@app.route("/challenge/hash/lasttry", methods=['GET'])
def getHashLastTry():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.args.get('userid')
    chid = request.args.get('chid')
    lastTry = db.getHashLastTry(userid, chid)
    if lastTry is None:
        return json.dumps({"error": "Unable to fetch cypher last try"})
    else:
        return json.dumps({"success": lastTry})


@app.route("/challenge/hash", methods=['POST'])
def addHashChallenge():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.form["userid"]
    tip = request.form["tip"]
    msg = request.form["msg"]
    algo = request.form["algo"]
    ok = db.addHashChallenge(userid, tip, msg, algo)
    return json.dumps({"success": ok})


@app.route("/challenge/hash/<chid>", methods=['PATCH'])
def updateHashChallenge(chid):
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    userid = request.form["userid"]
    date = request.form["date"]
    success = request.form['success']
    ok = db.updateHashChallengeTry(userid, chid, date, success)
    return json.dumps({"success": ok})


@app.route("/user/<userid>/challenges/count", methods=['GET'])
def getUserCreatedAmount(userid):
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    result = db.getUserCreatedAmount(userid)
    if result is None:
        return json.dumps({"error": "Unable to fetch user created amount"})
    else:
        return json.dumps({"success": result})


@app.route("/scoreboard", methods=['GET'])
def getScoreboard():
    try:
        ok = appAuth.authenticateApp(request.headers, request.method)
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({ "error": ex.message })
    
    table = db.getAllScoreboard()
    if table is None:
        return json.dumps({"error": "Unable to fetch scoreboard"})
    else:
        json_data=[]
        for result in table[1]:
            json_data.append(dict(zip(table[0],result)))
        return json.dumps({"success": json_data})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
