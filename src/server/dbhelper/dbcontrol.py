import hashlib
import binascii

from .mariadbhelper import *
from .tui.cli import crt

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


    def getHMACKey(self):
        return self._helper.config['VALIDATION']['hmac']


    def valueExists(self, table, field, value):
        self.start()
        self._helper                    \
            .Select([(field, None)])    \
            .From(table)                \
            .Where(f"{field}=?")        \
            .execute((value,))
        self._helper.resetQuery()
        ok = False
        for (c,) in self._helper.getCursor():
            ok = True
        self.stop()
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
        self.start()
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
        self.stop()
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), binascii.unhexlify(salt), 100000)
        if new_key == binascii.unhexlify(key):
            return (True, id_user)
        else:
            raise WrongPassword(f"Wrong password for user '{username}'.")


    def registerUser(self, username, password, email):
        # gera salt, calcula o sha256 (10000x) 
        self.start()
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
            self.stop()
            return False
        self._helper.resetQuery()
        self.stop()
        return True


    def addCypherChallenge(self, id_user, tip, msg, val, iv, hmacdb, algorithm):
        self.start()
        try:
            self._helper                                                            \
                .InsertInto(
                    "desafios_cifras",
                    ["id_user", "dica", "resposta", "texto_limpo", "iv", "hmac", "algoritmo"] )   \
                .execute((id_user, tip, msg, val, iv, hmacdb, algorithm))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            self.stop()
            return False
        self._helper.resetQuery()
        self.stop()
        return True


    def getAllCypherChallenges(self):
        self.start()
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_cifras.id_desafio_cifras", "ID"),
                    ("desafios_cifras.algoritmo", None),
                    ("utilizadores.username", "Proposto por")])                                 \
                .From("desafios_cifras")                                                        \
                .InnerJoin("utilizadores", on="desafios_cifras.id_user=utilizadores.id_user")   \
                .execute()
            row_headers=[x[0] for x in self._helper.getCursor().description]
            rv = self._helper.getCursor().fetchall()
            self._helper.resetQuery()
            self.stop()
            return (row_headers, rv)
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        self.stop()
        return None


    def getCypherChallenge(self, id_challenge):
        self.start()
        try:
            self._helper                                                                        \
                .Select([
                    ("desafios_cifras.resposta", None),
                    ("desafios_cifras.dica", None),
                    ("desafios_cifras.algoritmo", None),
                    ("desafios_cifras.texto_limpo", None),
                    ("desafios_cifras.iv", None),
                    ("desafios_cifras.hmac", None),
                    ("utilizadores.username", None)     ])                                      \
                .From("desafios_cifras")                                                        \
                .InnerJoin("utilizadores", on="desafios_cifras.id_user=utilizadores.id_user")   \
                .Where("id_desafio_cifras=?")                                                   \
                .execute((id_challenge,))
            self._helper.resetQuery()
            for (a, t, x, p, i, hm, u) in self._helper.getCursor():
                answer    = a
                tip       = t
                algorithm = x
                plaintext = p
                iv        = i
                hmacdb    = hm
                username  = u
            self.stop()
            return {
                'answer'    : answer,
                'tip'       : tip,
                'algorithm' : algorithm,
                'plaintext' : plaintext,
                'iv'        : iv,
                'hmac'      : hmacdb,
                'username'  : username
            }
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        self.stop()
        return None


    def getCypherLastTry(self, id_user, id_challenge):
        last_date = None
        self.start()
        try:
            self._helper                                    \
                .Select([("data_ultima_tentativa", None)])  \
                .From("utilizadores_cifras")                  \
                .Where("id_user=? AND id_desafio_cifras=?")   \
                .OrderBy(
                    predicate="data_ultima_tentativa",
                    desc=True,
                    limit=1
                ).execute((id_user, id_challenge))
            for (ld,) in self._helper.getCursor():
                last_date = ld
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
        self._helper.resetQuery()
        self.stop()
        return last_date


    def updateCypherChallengeTry(self, id_user, id_challenge, date, success):
        self.start()
        try:
            self._helper \
                .InsertInto(
                    table="utilizadores_cifras",
                    keys=[
                        "id_user",
                        "id_desafio_cifras",
                        "data_ultima_tentativa",
                        "sucesso"
                    ]
                ).execute((id_user, id_challenge, date, success))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            self.stop()
            return False
        self._helper.resetQuery()
        self.stop()
        return True


    def addHashChallenge(self, id_user, tip, msg, algorithm):
        self.start()
        try:
            self._helper                                            \
                .InsertInto(
                    "desafios_hash",
                    ["id_user", "dica", "resposta", "algoritmo"] )  \
                .execute((id_user, tip, msg, algorithm))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            self.stop()
            return False
        self._helper.resetQuery()
        self.stop()
        return True


    def getAllHashChallenges(self):
        self.start()
        try:
            self._helper                                                                    \
                .Select([
                    ("desafios_hash.id_desafio_hash", "ID"),
                    ("desafios_hash.algoritmo", None),
                    ("utilizadores.username", "Proposto por")])                             \
                .From("desafios_hash")                                                      \
                .InnerJoin("utilizadores", on="desafios_hash.id_user=utilizadores.id_user") \
                .execute()
            row_headers=[x[0] for x in self._helper.getCursor().description]
            rv = self._helper.getCursor().fetchall()
            self._helper.resetQuery()
            self.stop()
            return (row_headers, rv)
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
        self._helper.resetQuery()
        self.stop()
        return None


    def getHashChallenge(self, id_challenge):
        self.start()
        try:
            self._helper                                                                    \
                .Select([
                    ("desafios_hash.resposta", None),
                    ("desafios_hash.dica", None),
                    ("desafios_hash.algoritmo", None),
                    ("utilizadores.username", None),    ])                                  \
                .From("desafios_hash")                                                      \
                .InnerJoin("utilizadores", on="desafios_hash.id_user=utilizadores.id_user") \
                .Where("id_desafio_hash=?")                                                 \
                .execute((id_challenge,))
            for (a, t, x, u) in self._helper.getCursor():
                answer    = a
                tip       = t
                algorithm = x
                username  = u
            self.stop()
            return {
                'answer'    : answer,
                'tip'       : tip,
                'algorithm' : algorithm,
                'username'  : username
            }
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
        self._helper.resetQuery()
        self.stop()
        return None


    def getHashLastTry(self, id_user, id_challenge):
        last_date = None
        self.start()
        try:
            self._helper                                    \
                .Select([("data_ultima_tentativa", None)])  \
                .From("utilizadores_hash")                  \
                .Where("id_user=? AND id_desafio_hash=?")   \
                .OrderBy(
                    predicate="data_ultima_tentativa",
                    desc=True,
                    limit=1
                ).execute((id_user, id_challenge))
            for (ld,) in self._helper.getCursor():
                last_date = ld
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
        self._helper.resetQuery()
        self.stop()
        return last_date


    def updateHashChallengeTry(self, id_user, id_challenge, date, success):
        self.start()
        try:
            self._helper \
                .InsertInto(
                    table="utilizadores_hash",
                    keys=[
                        "id_user",
                        "id_desafio_hash",
                        "data_ultima_tentativa",
                        "sucesso"
                    ]
                ).execute((id_user, id_challenge, date, success))
            self._helper.commit()
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
            self.stop()
            return False
        self._helper.resetQuery()
        self.stop()
        return True


    def getAllScoreboard(self):
        self.start()
        try:
            self._helper \
                .AddCustomQuery(
"""
select
u.username as 'User',
CAST(if(a.CypherOK is null, 0, a.CypherOK) AS int) as 'Cypher',
CAST(if(a.HashOK is null, 0, a.HashOK) AS int) as 'Hash',
CAST(if(a.CypherOK is null, 0, a.CypherOK) + if(a.HashOK is null, 0, a.HashOK) as int) as 'Total'
from
(
select distinct
uc.id_user as 'CypherID',
sum(uc.sucesso) as 'CypherOK',
uc.id_desafio_cifras as 'CypherChal',
r.HashID,
r.HashOK,
r.HashChal
from utilizadores_cifras uc
left join
(
select distinct
uh.id_user as 'HashID',
sum(uh.sucesso) as 'HashOK',
uh.id_desafio_hash as 'HashChal'
from utilizadores_hash uh
where uh.sucesso=1
group by uh.id_user
) r on r.HashID = uc.id_user
where uc.sucesso=1
group by uc.id_user
) a
left join utilizadores u on u.id_user = a.CypherID
order by Total desc
"""
                ).execute()
            row_headers=[x[0] for x in self._helper.getCursor().description]
            rv = self._helper.getCursor().fetchall()
            self._helper.resetQuery()
            self.stop()
            return (row_headers, rv)
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
        self._helper.resetQuery()
        self.stop()
        return None


    def getEmail(self, id_user):
        self.start()
        try:
            self._helper                    \
                .Select([("email", None)])  \
                .From("utilizadores")       \
                .Where("id_user = ?")       \
                .execute((id_user,))
            self._helper.resetQuery()
            for (email,) in self._helper.getCursor():
                useremail = email
            self.stop()
            return useremail
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        self.stop()
        return None
    
    
    def getUserCreatedAmount(self, id_user):
        self.start()
        try:
            self._helper\
                .AddCustomQuery(
"""
select
    count(dc.id_desafio_cifras) as 'Cypher',
    r.Hash,
    count(dc.id_desafio_cifras) + r.Hash as 'Total'
from desafios_cifras dc
left join (
select 
    count(dh.id_desafio_hash) as 'Hash'
from desafios_hash dh
where dh.id_user = ?
) r on true
where dc.id_user = ?
"""
                ).execute((id_user, id_user))
            self._helper.resetQuery()
            for (c, h, total) in self._helper.getCursor():
                Cypher = c
                Hash   = h
                Total  = total
            self.stop()
            return {
                'cypher': Cypher,
                'hash':   Hash,
                'total':  Total
            }
        except mariadb.Error as ex:
            crt.writeError(f"Error at database: {ex}")
            self._helper.resetQuery()
        self.stop()
        return None
    