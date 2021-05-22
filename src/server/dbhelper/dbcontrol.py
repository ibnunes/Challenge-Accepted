import hashlib
import binascii

from .mariadbhelper import *
from .tui.cli import crt


class UsernameNotFound(Exception):
    """Exception UsernameNotFound."""
    def __init__(self, message="Username not found"):
        self.message = message
        super().__init__(self.message)


class WrongPassword(Exception):
    """Exception WrongPassword."""
    def __init__(self, message="Wrong password"):
        self.message = message
        super().__init__(self.message)


class DBControl(object):
    def __init__(self):
        """Initializes DBControl."""        
        self._helper = MariaDBHelper()
        self._helper.bindErrorCallback(crt.writeError)


    def start(self):
        """
        Starts DBControl.

        Raises:
            ConnectionNotEstablished: raised when MariaDBHelper isn't connected
        """
        self._helper.connect()
        if not self._helper.isConnected():
            raise ConnectionNotEstablished()


    def stop(self):
        """Stops DBControl."""        
        if self._helper.isConnected():
            self._helper.disconnect()

    def fetchAppId(self, appId):
        """
        Fetchs App ID.
        WHERE THE HELL IS THIS CALLED???

        Args:
            appId (int): Application ID

        Returns:
            [type]: [description] 
        """        
        self.start()
        self._helper                    \
            .Select([("`key`", None)])  \
            .From("apps")               \
            .Where("appid=?")           \
            .execute((appId,))

        self._helper.resetQuery()

        try:
            record = self._helper.getCursor().next()[0]
            #for (r,) in self._helper.getCursor():
            #    record = r
            self.stop()
            return record
        except (StopIteration, Exception, mariadb.Error):
            self.stop()
            return None


    def getHMACKey(self):
        """
        Gets HMAC Key from the config.

        Returns:
            str: HMAC key
        """        
        return self._helper.config['VALIDATION']['hmac']


    def valueExists(self, table, field, value):
        """
        Checks if value exists.

        Args:
            table (str): Table
            field (str): Field
            value (str): Value

        Returns:
            bool: True IF exists ELSE False
        """        
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
        """
        Checks if user exists.

        Args:
            username (str): Username

        Returns:
            bool: True IF exists ELSE False
        """
        return self.valueExists(
            table = "utilizadores",
            field = "username",
            value = username
        )


    def emailExists(self, email):
        """
        Checks if an email already exists.

        Args:
            email (str): email

        Returns:
            bool: True IF exists ELSE False
        """
        return self.valueExists(
            table = "utilizadores",
            field = "email",
            value = email
        )


    def loginUser(self, username, password):
        """
        Logs the user in.

        Args:
            username (str): Username
            password (str): Password

        Raises:
            Exception:        Generic Exception
            UsernameNotFound: Could not find username
            WrongPassword:    Wrong Password

        Returns:
            (bool, int): (Success, User ID)
        """
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
        """
        Registers User.
        Generates salt, calculates sha256 (10000x)

        Args:
            username (str): Username
            password (str): Password
            email (str): Email

        Returns:
            bool: True IF successful ELSE False
        """
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
        """
        Adds cypher challenge.

        Args:
            id_user (int): User ID
            tip (str): Challenge Tip
            msg (str): Message
            val (str): Value
            iv (str): Inicializer Vector
            hmacdb (str): HMAC
            algorithm (str): Algorithm

        Returns:
            bool: True IF successful ELSE False
        """        
        self.start()
        try:
            self._helper                                                                          \
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
        """
        Gets every cypher challenge.

        Returns:
            (list, Any): Row Headers, Row Values
            None: When failed
        """
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
        """
        Gets cypher challenge.

        Args:
            id_challenge (int): Challenge ID

        Returns:
            dict: {
                'answer': Answer, 
                'tip': , 
                'algorithm': Challenge algorithm, 
                'plaintext': Plain Text,
                'iv': Initialized Vector,
                'hmac': HMAC,
                'username': Username
            }
            None: When failed
        """
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
        """
        Gets last try of cypher.

        Args:
            id_user (int): UserID
            id_challenge (int): ChallengeID

        Returns:
            float: Last Date of an attempt
        """
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
        """
        Adds attempt of concluding a challenge.

        Args:
            id_user (int): UserID
            id_challenge (int): ChallengeID
            date (float): Date of the attempt
            success (bool): Success

        Returns:
            bool: True IF successful ELSE False
        """
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
        """
        Adds hash challenge.

        Args:
            id_user (int): UserID
            tip (str): Tip
            msg (str): Message
            algorithm (str): Algorithm

        Returns:
            bool: True IF successful ELSE False
        """
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
        """
        Gets every cypher challenge.

        Returns:
            (list, Any): Row Headers, Row Values
            None: When failed
        """
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
        """
        Gets hash challenge.

        Args:
            id_challenge (int): Challenge ID

        Returns:
            dict: {
                'answer': str,
                'tip': str,
                'algorithm': str,
                'username': str
            }
            None: When fails 
        """        
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
        """
        Gets last try of hash challenge.

        Args:
            id_user (int): UserID
            id_challenge (int): ChallengeID

        Returns:
            float: Last Date of an attempt
        """
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
        """
        Adds attempt of concluding a challenge.

        Args:
            id_user (int): UserID
            id_challenge (int): ChallengeID
            date (float): Date of the attempt
            success (bool): Success

        Returns:
            bool: True IF successful ELSE False
        """
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
        """Gets all scores."""
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
        """
        Gets Email.

        Args:
            id_user (str): User ID

        Returns:
            str: User's Email
            None: When fails
        """        
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
        """
        Gets user created challenges amount.

        Args:
            id_user (int): User ID
            
        Returns:
            dict: {
                'cypher': int,
                'hash':   int,
                'total':  int
            }
            None: when fails
        """        
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
    
