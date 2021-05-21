from prettytable import PrettyTable
from prettytable import from_json

from .mariadbhelper import *
from tui.cli import crt
import utils.remote as remote

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


    def start(self, url=None, port=None):
        if url is not None:
            self._url = "http://" + url
        if port is not None:
            self._url += f":{port}"
        crt.writeDebug(self._url)


    def stop(self):
        pass


    def userExists(self, username):
        r = requests.post(
            f"{self._url}/auth/user",
            data={'username' : username}
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def emailExists(self, email):
        r = requests.post(
            f"{self._url}/auth/email",
            data={'email' : email}
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def loginUser(self, username, password):
        r = requests.post(
            f"{self._url}/auth/login",
            data={'username' : username, 'password' : password}
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if not ok:
            raise StatusCodeError(data)
        return (ok, data['user_id'])


    def registerUser(self, username, password, email):
        r = requests.post(
            f"{self._url}/auth/signup",
            data={'username' : username, 'password' : password, 'email': email}
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return ok


    def addCypherChallenge(self, id_user, tip, msg, val, algorithm):
        r = requests.post(
            f"{self._url}/challenge/cypher",
            data={
                'userid' : id_user,
                'tip'    : tip,
                'msg'    : msg,
                'val'    : val,
                'algo'   : algorithm
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def getAllCypherChallenges(self):
        pt = PrettyTable()
        r = requests.get(
            f"{self._url}/challenge/cypher"
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        return pt


    def getCypherChallenge(self, id_challenge):
        r = requests.get(f"{self._url}/challenge/cypher/{id_challenge}")
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None


    def getCypherLastTry(self, id_user, id_challenge):
        r = requests.get(
            f"{self._url}/challenge/cypher/lasttry",
            params={
                "userid" : id_user,
                "chid"   : id_challenge
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None


    def updateCypherChallengeTry(self, id_user, id_challenge, date):
        r = requests.patch(
            url="{self._url}/challenge/cypher/{id_challenge}",
            params={
                "userid" : id_user,
                "date"   : date
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def addHashChallenge(self, id_user, tip, msg, algorithm):
        r = requests.post(
            f"{self._url}/challenge/hash",
            data={
                'userid' : id_user,
                'tip'    : tip,
                'msg'    : msg,
                'algo'   : algorithm
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def getAllHashChallenges(self):
        pt = PrettyTable()
        r = requests.get(
            f"{self._url}/challenge/hash"
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        return pt


    def getHashChallenge(self, id_challenge):
        r = requests.get(f"{self._url}/challenge/hash/{id_challenge}")
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None


    def getHashLastTry(self, id_user, id_challenge):
        r = requests.get(
            f"{self._url}/challenge/hash/lasttry",
            params={
                "userid" : id_user,
                "chid"   : id_challenge
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None


    def updateHashChallengeTry(self, id_user, id_challenge, date):
        r = requests.patch(
            url="{self._url}/challenge/hash/{id_challenge}",
            params={
                "userid" : id_user,
                "date"   : date
            }
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        return data


    def getAllScoreboard(self):
        pt = PrettyTable()
        r = requests.get(f"{self._url}/scoreboard")
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            pt = from_json(json.dumps(data))
        return pt


    def getEmail(self, id_user):
        r = requests.get(
            f"{self._url}/user/email",
            params={'id' : id_user}
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None


    def getUserCreatedAmount(self, id_user):
        r = requests.get(
            f"{self._url}/user/{id_user}/challenges/count"
        )
        if r.status_code != 200:
            raise StatusCodeError(str(r.status_code))
        (ok, data) = remote.unpack(r.json())
        if ok:
            return data
        return None
