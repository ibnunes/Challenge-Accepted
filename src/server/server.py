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
    """
    * Description: Gets HMAC Key.
    * Endpoint:    `/auth/hmac`
    * HTTP Method: ``GET``
    
    Possible Success:
    * `{"success" : (str)}` - Returns HMAC.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                    - Exception 
    * `{"error" : "Unknown error authenticating app"}` - Unable to authenticate the app
    * `{"error" : "Username not found"}`               - UsernameNotFound
    * `{"error" : "Wrong passowrd"}`                   - WrongPassword
    """
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
    """
    * Description: Authenticates a User using `username` and `password` combination.
    * Endpoint:    `/auth/login`
    * HTTP Method: ``POST``
    
    Possible Success:
    * `{"success" : { "user_id" : user_id }}` - Returns dictionary with the user_id.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                    - Exception 
    * `{"error" : "Unknown error authenticating app"}` - Unable to authenticate the app
    * `{"error" : "Username not found"}`               - UsernameNotFound
    * `{"error" : "Wrong passowrd"}`                   - WrongPassword
    """
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
    """
    * Description: Creates a new User using `username`, `email`, `password` combination.
    * Endpoint:    `/auth/signup`
    * HTTP Method: ``POST``
    
    Possible Success:
    * `{"success" : { "user_id" : user_id }}` - Returns dictionary with the user_id.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                    - Exception 
    * `{"error" : "Unknown error authenticating app"}` - Unable to authenticate the app
    * `{"error" : "Username not found"}`               - UsernameNotFound
    * `{"error" : "Wrong passowrd"}`                   - WrongPassword
    """
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
    """
    * Description: Checks if a username is already in use.
    * Endpoint:    `/auth/user`
    * HTTP Method: ``POST``
    
    Possible Success:
    * `{ "success" : (bool) }` - Returns True IF `username` exists ELSE False.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception
    * `{"error" : "Unknown error authenticating app"}`     - Unable to Authenticate the App
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Checks if an email is already in use.
    * Endpoint:    `/auth/user`
    * HTTP Method: ``POST``
    
    Possible Success:
    * `{ "success" : (bool) }` - Returns True if `email` exists else False.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to Authenticate the App
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets the email of an user using `user_id` as `id`.
    * Endpoint:    `/user/email`
    * HTTP Method: ``GET``
    
    Possible Success:
    * `{ "success" : (str) }` - Returns the email.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch email"}`                - Unable to fetch email
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets every cypher challenge available.
    * Endpoint:    `/challenge/cypher`
    * HTTP Method: ``GET``
    
    Possible Success:
    * `{ "success" : (list) }` - Returns list of dictionaries with the results table.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch cypher challenges"}`    - Unable to fetch cypher challenges
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets specific cypher challenge with the use of `challenge_id` as `chid`.
    * Endpoint:    `/challenge/cypher/<chid>`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ 
            "success" : {
                'answer'    : (str),
                'tip'       : (str),
                'algorithm' : (str),
                'plaintext' : (str),
                'iv'        : (int),
                'hmac'      : (str),
                'username'  : (str)
           } 
         }``` - Returns dictionary with specified cypher challenge data
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch cypher challenge"}`     - Unable to fetch cypher challenge
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets date of last time a `user` as `userid` attempted to solve a `challenge` as `chid`. 
    * Endpoint:    `/challenge/cypher/lasttry`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ "success" : (float)}``` - Returns date of last attempt to conclude a challenge
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch cypher last try"}`      - Unable to fetch cypher last try
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Adds cypher challenge to the Database. 
    * Endpoint:    `/challenge/cypher`
    * HTTP Method: ``POST``
    
    Possible Success:
    * ```{ "success" : (bool)}``` - Returns True IF saved with success ELSE False
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
    try:
        ok = appAuth.authenticateApp(request.headers, request.method, dict(request.form))
        if not ok:
            return json.dumps({ "error": "Unknown error authenticating app" })
    except (ConnectionNotEstablished, InvalidAppAuthenticationChallenge, AppAuthHeaderNotFound) as ex:
        return json.dumps({"error": ex.message })
    
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
    """
    * Description: Adds attempt of concluding a challenge using User as `userid`, 
    Challenge as `chid`, Date as `date` and Success as `success` 
    * Endpoint:    `/challenge/cypher/<chid>`
    * HTTP Method: ``PATCH``
    
    Possible Success:
    * ```{ "success" : (bool)}``` - Returns True IF added with success ELSE False
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets every hash challenge available.
    * Endpoint:    `/challenge/hash`
    * HTTP Method: ``GET``
    
    Possible Success:
    * `{ "success" : (list) }` - Returns list of dictionaries with the results table.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch hash challenges"}`      - Unable to fetch hash challenges
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets specific hash challenge with the use of Challenge as `chid`.
    * Endpoint:    `/challenge/hash/<chid>`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ 
            "success" : {
                'answer'    : (str),
                'tip'       : (str),
                'algorithm' : (str),
                'username'  : (str)
            }
         }``` - Returns dictionary with specified hash challenge data
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch hash challenge"}`       - Unable to fetch hash challenge
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets date of last time a User as `userid` attempted to solve a Hash Challenge as `chid`. 
    * Endpoint:    `/challenge/hash/lasttry`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ "success" : (float)}``` - Returns date of last attempt to conclude a challenge
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch hash last try"}`        - Unable to fetch hash last try
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Adds hash challenge to the Database. 
    * Endpoint:    `/challenge/hash`
    * HTTP Method: ``POST``
    
    Possible Success:
    * ```{ "success" : (bool)}``` - Returns True IF saved with success ELSE False
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Adds attempt of concluding a hash challenge using User as `userid`, 
    Challenge as `chid`, Date as `date` and Success as `success` 
    * Endpoint:    `/challenge/hash/<chid>`
    * HTTP Method: ``PATCH``
    
    Possible Success:
    * ```{ "success" : (bool)}``` - Returns True IF added with success ELSE False
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Gets the amount of challenges created by a User.
    * Endpoint:    `/challenge/hash/<chid>`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ "success" : {
                'cypher': (int),
                'hash':   (int),
                'total':  (int)
            }
        }``` - Returns dictionary with all the created amounts
    
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unable to fetch user created amount"}`  - Unable to fetch user created amount
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
    """
    * Description: Adds attempt of concluding a hash challenge using User as `userid`, 
    Challenge as `chid`, Date as `date` and Success as `success` 
    * Endpoint:    `/challenge/hash/<chid>`
    * HTTP Method: ``GET``
    
    Possible Success:
    * ```{ "success" : list()}``` - Returns list of dictionaries with the results table.
    
    Possible Errors:
    * `{"error" : "Unknown Error"}`                        - Exception 
    * `{"error" : "Unknown error authenticating app"}`     - Unable to authenticate the app
    * `{"error" : "Unable to fetch scoreboard"}`           - Unable to fetch scoreboard
    * `{"error" : "Connection not established"}`           - ConnectionNotEstablished
    * `{"error" : "Invalid App Authentication Challenge"}` - InvalidAppAuthenticationChallenge
    * `{"error" : "App Auth Header Not Found"}`            - AppAuthHeaderNotFound
    """
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
