from prettytable import PrettyTable
from prettytable import from_json
import prettytable
from requests.api import head

from tui.cli import crt
from utils.remote import unpack
from utils.appauth import AppAuthenticationClient

import json
import requests


class UsernameNotFound(Exception):
    def __init__(self, message="Username not found"):
        self.message = message
        super().__init__(self.message)


class WrongPassword(Exception):
    def __init__(self, message="Wrong password"):
        self.message = message
        super().__init__(self.message)


class StatusCodeError(Exception):
    def __init__(self, message="Status Code not 200"):
        self.message = message
        super().__init__(self.message)


class DBControl(object):
    def __init__(self):
        self._url  = "localhost:80"
        self._appauth = AppAuthenticationClient("9556bd24-fa30-41f0-8af8-fd1b3b9f6500", "Zyoz46m7IosX1RILxtghjxRqpch5FQlj80VE4d1OiNIo")


    def start(self, url=None, port=None):
        if url is not None:
            self._url = url
        if port is not None:
            self._url += f":{port}"
        crt.writeDebug(self._url)


    def stop(self):
        pass


    def getHMACKey(self):
        r = requests.get(
            url=f"{self._url}/auth/hmac",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return bytes(data, 'utf-8')
        else:
            raise Exception(data)


    def userExists(self, username):
        data = {'username' : username}
        r = requests.post(
            url=f"{self._url}/auth/user",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def emailExists(self, email):
        data = {'email' : email}
        r = requests.post(
            url=f"{self._url}/auth/email",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def loginUser(self, username, password):
        data = {'username' : username, 'password' : password}
        r = requests.post(
            url=f"{self._url}/auth/login",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if not ok:
            raise StatusCodeError(data)
        return (ok, data['user_id'])


    def registerUser(self, username, password, email):
        data = {'username' : username, 'password' : password, 'email': email}
        r = requests.post(
            url=f"{self._url}/auth/signup",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return ok


    def addCypherChallenge(self, id_user, tip, msg, val, iv, hmacdb, algorithm):
        data = {
                'userid' : id_user,
                'tip'    : tip,
                'msg'    : msg,
                'val'    : val,
                'iv'     : iv,
                'hmac'   : hmacdb,
                'algo'   : algorithm
            }
        r = requests.post(
            url=f"{self._url}/challenge/cypher",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def getAllCypherChallenges(self):
        pt = PrettyTable()
        r = requests.get(
            url=f"{self._url}/challenge/cypher",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        return pt


    def getCypherChallenge(self, id_challenge):
        r = requests.get(
            url=f"{self._url}/challenge/cypher/{id_challenge}",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None


    def getCypherLastTry(self, id_user, id_challenge):
        r = requests.get(
            url=f"{self._url}/challenge/cypher/lasttry",
            params={
                "userid" : id_user,
                "chid"   : id_challenge
            },
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None


    def updateCypherChallengeTry(self, id_user, id_challenge, date, success):
        data = {
                "userid"  : id_user,
                "date"    : date,
                "success" : 1 if success else 0
            }
        r = requests.patch(
            url=f"{self._url}/challenge/cypher/{id_challenge}",
            data=data,
            headers=self._appauth.generatePatchHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def addHashChallenge(self, id_user, tip, msg, algorithm):
        data = {
                'userid' : id_user,
                'tip'    : tip,
                'msg'    : msg,
                'algo'   : algorithm
            }
        r = requests.post(
            url=f"{self._url}/challenge/hash",
            data=data,
            headers=self._appauth.generatePostHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def getAllHashChallenges(self):
        pt = PrettyTable()
        r = requests.get(
            url=f"{self._url}/challenge/hash",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        return pt


    def getHashChallenge(self, id_challenge):
        r = requests.get(
            url=f"{self._url}/challenge/hash/{id_challenge}",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None


    def getHashLastTry(self, id_user, id_challenge):
        r = requests.get(
            url=f"{self._url}/challenge/hash/lasttry",
            params={
                "userid" : id_user,
                "chid"   : id_challenge
            },
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None


    def updateHashChallengeTry(self, id_user, id_challenge, date, success):
        data = {
                "userid"  : id_user,
                "date"    : date,
                "success" : 1 if success else 0
            }
        r = requests.patch(
            url=f"{self._url}/challenge/hash/{id_challenge}",
            data=data,
            headers=self._appauth.generatePatchHeader(data)
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        return data


    def getAllScoreboard(self):
        pt = PrettyTable()
        r = requests.get(
            url=f"{self._url}/scoreboard",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        else:
            crt.writeDebug(str(data))
        return pt


    def getEmail(self, id_user):
        r = requests.get(
            url=f"{self._url}/user/email",
            params={'id' : id_user},
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None


    def getUserCreatedAmount(self, id_user):
        r = requests.get(
            url=f"{self._url}/user/{id_user}/challenges/count",
            headers=self._appauth.generateGetHeader()
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = unpack(r.json())
        if ok:
            return data
        return None
