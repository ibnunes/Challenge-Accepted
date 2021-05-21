from dbhelper.mariadbhelper import *
from dbhelper.dbcontrol import *
import time
import uuid
import hashlib
import json
import hmac

class AppIdNotFound(Exception):
    def __init__(self, message="App ID not found"):
        self.message = message
        super().__init__(self.message)

class AppAuthHeaderNotFound(Exception):
    def __init__(self, message="App authentication header not found"):
        self.message = message
        super().__init__(self.message)

class InvalidAppAuthenticationChallenge(Exception):
    def __init__(self, message="Invalid app authentication challenge"):
        self.message = message
        super().__init__(self.message)

class NotConnected(Exception):
    def __init__(self, message="Inable to conenct to database"):
        self.message = message
        super().__init__(self.message)

class AppAuthenticationServer(object):
    def __init__(self):
        self._db = DBControl()        

    def authenticateApp(self, headers, method="GET", body=None):
        try:
            appid = headers["appid"]
            appKey = self._db.fetchAppId(appid)
            timestamp = headers["timestamp"]
            nonce = headers["nonce"]
            sign = headers["sig"]

            if appKey is None:
                raise AppIdNotFound()

            if method == "GET":
                if self.compareGetSig(timestamp, nonce, appid, appKey, sign):
                    return True
            elif method == "POST":
                if self.generatePostSig(timestamp, nonce, appid, appKey, sign, body):
                    return True
            elif method == "PATCH":
                if self.comparePatchSig(timestamp, nonce, appid, appKey, sign, body):
                    return True
            raise InvalidAppAuthenticationChallenge()
        except (ConnectionNotEstablished):
            raise NotConnected()
        except (KeyError):
            raise AppAuthHeaderNotFound()

    def getHeaders(self, request):
        try:
            appid = request.headers['appid']
            timestamp = request.headers['timestamp']
            nonce = request.headers['nonce']
            sign = request.headers['sig']
            return (appid, timestamp, nonce, sign)
        except (KeyError):
            raise AppAuthHeaderNotFound()

    def generatePostSig(self, timestamp, nonce, appId, key, hsig, body):
        bodyHash = hashlib.sha256(json.dumps(body).encode('utf-8')).hobj.hexdigest()
        sign = "{appid}POST{timestamp}{nonce}{bodyHash}".format(appid = appId, timestamp = timestamp, nonce = nonce, bodyHash = bodyHash)
        hmacsh256 = hmac.new(key=key.encode('utf-8'), msg=sign.encode('utf-8'), digestmod=hashlib.sha256)
        return hmacsh256 == hsig

    def comparePatchSig(self, timestamp, nonce, appId, key, hsig, body):
        bodyHash = hashlib.sha256(json.dumps(body).encode('utf-8')).hobj.hexdigest()
        sign = "{appid}PATCH{timestamp}{nonce}{bodyHash}".format(appid = appId, timestamp = timestamp, nonce = nonce, bodyHash = bodyHash)
        hmacsh256 = hmac.new(key=key.encode('utf-8'), msg=sign.encode('utf-8'), digestmod=hashlib.sha256)
        return hmacsh256 == hsig

    def compareGetSig(self, timestamp, nonce, appId, key, hsig):
        sign = "{appid}GET{timestamp}{nonce}".format(appid = appId, timestamp = timestamp, nonce = nonce)
        hmacsh256 = hmac.new(key=key.encode('utf-8'), msg=sign.encode('utf-8'), digestmod=hashlib.sha256)
        return hmacsh256.hexdigest() == hsig