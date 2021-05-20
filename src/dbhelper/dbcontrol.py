import hashlib
import binascii

from .mariadbhelper import *
from tui.cli import crt


class UsernameNotFound(Exception):
    def __init__(self, message="Username not found"):
        self.message = message
        super().__init__(self.message)


class WrongPassword(Exception):
    def __init__(self, message="Wrong password"):
        self.message = message
        super().__init__(self.message)


class DBControl(object):
    def __init__(self):
        self._helper = MariaDBHelper()
        self._helper.bindErrorCallback(crt.writeError)


    def start(self):
        self._helper.connect()
        if not self._helper.isConnected():
            raise ConnectionNotEstablished()


    def stop(self):
        if self._helper.isConnected():
            self._helper.disconnect()


    def userExists(self, username):
        self._helper \
            .Select([("username", None)]) \
            .From("utilizadores") \
            .Where("username=?") \
            .execute((username,))
        self._helper.resetQuery()
        ok = False
        for (c,) in self._helper.getCursor():
            ok = True
        return ok


    def loginUser(self, username, password):
        uname, key, salt = "", "", ""
        self._helper \
            .Select([("id_user", None), ("password", None), ("salt", None)]) \
            .From("utilizadores") \
            .Where("username=?") \
            .execute((username,))
        
        try:
            for (x, y, z) in self._helper.getCursor():
                (id_user, key, salt) = (x, y, z)
        except (Exception, mariadb.Error) as ex:
            raise UsernameNotFound(f"User '{username}' does not exist.")
        
        self._helper.resetQuery()
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), binascii.unhexlify(salt), 100000)
        if new_key == binascii.unhexlify(key):
            return True
        else:
            raise WrongPassword(f"Wrong password for user '{username}'.")


    def registerUser(self, username, password, email):
        # gera salt, calcula o sha256 (10000x) 
        salt = os.urandom(32)   # A new salt for this user
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self._helper \
            .InsertInto("utilizadores", ["username, email, password, salt"]) \
            .execute((username, email, binascii.hexlify(key), binascii.hexlify(salt)))
        self._helper.resetQuery()
        return True