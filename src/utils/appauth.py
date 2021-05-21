import time
import uuid
import hashlib
import json
import hmac

class AppAuthenticationClient(object):
    def __init__(self, appId, appKey):
        self._appId = appId
        self._appKey = appKey
    
    def generatePostHeader(self, body):
        timestamp = int(time.time())
        nonce = uuid.uuid4()
        bodyHash = hashlib.sha256(json.dumps(body).encode('utf-8')).hobj.hexdigest()
        sign = "{appid}POST{timestamp}{nonce}{bodyHash}".format(appid = self._appId, timestamp = timestamp, nonce = nonce, bodyHash = bodyHash)
        hmacsh256 = hmac.new(key=self._appKey.encode(), msg=sign.encode(), digestmod=hashlib.sha256)
        return { "timestamp": timestamp, "nonce": nonce, "sig": hmacsh256.hexdigest(), "appid": self._appId }

    def generatePatchHeader(self, body):
        timestamp = int(time.time())
        nonce = uuid.uuid4()
        bodyHash = hashlib.sha256(json.dumps(body).encode('utf-8')).hobj.hexdigest()
        sign = "{appid}PATCH{timestamp}{nonce}{bodyHash}".format(appid = self._appId, timestamp = timestamp, nonce = nonce, bodyHash = bodyHash)
        hmacsh256 = hmac.new(key=self._appKey.encode(), msg=sign.encode(), digestmod=hashlib.sha256)
        return { "timestamp": timestamp, "nonce": nonce, "sig": hmacsh256.hexdigest(), "appid": self._appId }

    def generateGetHeader(self):
        timestamp = int(time.time())
        nonce = uuid.uuid4()
        sign = "{appid}PATCH{timestamp}{nonce}".format(appid = self._appId, timestamp = timestamp, nonce = nonce)
        hmacsh256 = hmac.new(key=self._appKey.encode(), msg=sign.encode(), digestmod=hashlib.sha256)
        return { "timestamp": timestamp, "nonce": nonce, "sig": hmacsh256.hexdigest(), "appid": self._appId }