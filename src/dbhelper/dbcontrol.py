import hashlib
import binascii
from prettytable import PrettyTable
from prettytable import from_db_cursor

from .mariadbhelper import *
from tui.cli import crt

"""
TODO: - Documentation
"""

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


    def valueExists(self, table, field, value):
        self._helper                    \
            .Select([(field, None)])    \
            .From(table)                \
            .Where(f"{field}=?")        \
            .execute((value,))
        self._helper.resetQuery()
        ok = False
        for (c,) in self._helper.getCursor():
            ok = True
        return ok


    def userExists(self, username):
        return self.valueExists(
            table = "utilizadores",
            field = "username",
            value = username
        )


    def emailExists(self, email):
        return self.valueExists(
            table = "utilizadores",
            field = "email",
            value = email
        )


    def loginUser(self, username, password):
        key, salt = "", ""
        self._helper \
            .Select([("id_user", None), ("password", None), ("salt", None)]) \
            .From("utilizadores") \
            .Where("username=?") \
            .execute((username,))
        
        self._helper.resetQuery()

        try:
            for (x, y, z) in self._helper.getCursor():
                (id_user, key, salt) = (x, y, z)
            if (password == "" or salt == ""):
                raise Exception()
        except (Exception, mariadb.Error) as ex:
            raise UsernameNotFound(f"User '{username}' does not exist.")
        
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), binascii.unhexlify(salt), 100000)
        if new_key == binascii.unhexlify(key):
            return (True, id_user)
        else:
            raise WrongPassword(f"Wrong password for user '{username}'.")


    def registerUser(self, username, password, email):
        # gera salt, calcula o sha256 (10000x) 
        salt = os.urandom(32)   # A new salt for this user
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        try:
            self._helper \
                .InsertInto("utilizadores", ["username", "email", "password", "salt"]) \
                .execute((username, email, binascii.hexlify(key), binascii.hexlify(salt),))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            return False
        self._helper.resetQuery()
        return True


    def addCypherChallenge(self, id_user, tip, msg, val, algorithm):
        try:
            self._helper                                                            \
                .InsertInto(
                    "desafios_cifras",
                    ["id_user", "dica", "resposta", "texto_limpo", "algoritmo"] )   \
                .execute((id_user, tip, msg, val, algorithm))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            return False
        self._helper.resetQuery()
        return True


    def getAllCypherChallenges(self):
        pt = PrettyTable()
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_cifras.id_desafio_cifras", "ID"),
                    ("desafios_cifras.algoritmo", None),
                    ("utilizadores.username", "Proposto por")])                                 \
                .From("desafios_cifras")                                                        \
                .InnerJoin("utilizadores", on="desafios_cifras.id_user=utilizadores.id_user")   \
                .execute()
            pt = from_db_cursor(self._helper.getCursor())
            self._helper.resetQuery()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        return pt


    def getCypherChallenge(self, id_challenge):
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_cifras.resposta", None),
                    ("desafios_cifras.dica", None),
                    ("desafios_cifras.algoritmo", None),
                    ("desafios_cifras.texto_limp", None),
                    ("utilizadores.username", None)     ])                                      \
                .From("desafios_cifras")                                                        \
                .InnerJoin("utilizadores", on="desafios_cifras.id_user=utilizadores.id_user")   \
                .Where("id_desafio_cifras=?")                                                   \
                .execute((id_challenge,))
            self._helper.resetQuery()
            for (a, t, x, p, u) in self._helper.getCursor():
                answer    = a
                tip       = t
                algorithm = x
                plaintext = p
                username  = u
            return {
                'answer'    : answer,
                'tip'       : tip,
                'algorithm' : algorithm,
                'plaintext' : plaintext,
                'username'  : username
            }
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        return None


    def addHashChallenge(self, id_user, tip, msg, algorithm):
        try:
            self._helper                                                            \
                .InsertInto(
                    "desafios_hash",
                    ["id_user", "dica", "resposta", "algoritmo"] )   \
                .execute((id_user, tip, msg, algorithm))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            return False
        self._helper.resetQuery()
        return True


    def getAllHashChallenges(self):
        pt = PrettyTable()
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_hash.id_desafio_hash", "ID"),
                    ("desafios_hash.algoritmo", None),
                    ("utilizadores.username", "Proposto por")])                                 \
                .From("desafios_hash")                                                        \
                .InnerJoin("utilizadores", on="desafios_hash.id_user=utilizadores.id_user")   \
                .execute()
            pt = from_db_cursor(self._helper.getCursor())
            self._helper.resetQuery()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        return pt


    def getHashChallenge(self, id_challenge):
        return None
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_cifras.resposta", None),
                    ("desafios_cifras.dica", None),
                    ("desafios_cifras.algoritmo", None),
                    ("desafios_cifras.texto_limp", None),
                    ("utilizadores.username", None)     ])                                      \
                .From("desafios_cifras")                                                        \
                .InnerJoin("utilizadores", on="desafios_cifras.id_user=utilizadores.id_user")   \
                .Where("id_desafio_cifras=?")                                                   \
                .execute((id_challenge,))
            self._helper.resetQuery()
            for (a, t, x, p, u) in self._helper.getCursor():
                answer    = a
                tip       = t
                algorithm = x
                plaintext = p
                username  = u
            return {
                'answer'    : answer,
                'tip'       : tip,
                'algorithm' : algorithm,
                'plaintext' : plaintext,
                'username'  : username
            }
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        return None