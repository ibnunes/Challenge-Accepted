from Crypto.Cipher import AES
import hashlib
import Padding
import base64
import hmac
import secrets
# from prettytable import PrettyTable

# from app import App
from login.user import User
from utils.crypto import Cypher
from utils.read import Read
from utils.clock import Clock
from tui.cli import crt

"""
TODO: colocar na base de dados que teve sucesso
"""

class ChallengeCypher(object):
    APP = None

    @staticmethod
    def bindApp(app):
        """
        Binds Challenge with the app.

        Args:
            app (App): Application
        """
        ChallengeCypher.APP = app


    @staticmethod
    def add(user : User, algorithm):
        """
        Adds Challenge.

        Args:
            user (User): Author
            algorithm (str): given type of algorithm 

        Returns:
            bool: if not logged in returns false
        """
        if not user.isLoggedIn():
            return False
        
        val = Read.asString("Message: ")

        if algorithm == Cypher.Caesar.TYPE:
            password_caesar = Read.tryAsInt("Cypher key (number): ")
            password = str(password_caesar)
        else:
            while True:
                password = Read.asString("Cypher key: ")
                if (algorithm == Cypher.OTP.TYPE) and (len(val) != len(password)):
                    crt.writeWarning("Message and cypher key must have same length!")
                else:
                    break
        
        tip = Read.asString("[Optional] Tip / Help: ")
        
        plaintext = val
        key       = hashlib.md5(password.encode()).digest()
        iv        = secrets.token_hex(8)
        hmackey   = ChallengeCypher.APP.getDBController().getHMACKey()
        msgHMAC   = hmac.new(hmackey, val.encode(), hashlib.sha256).hexdigest()
        
        if algorithm == Cypher.ECB.TYPE:
            plaintext  = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)
            ciphertext = Cypher.ECB.encrypt(plaintext.encode(), key, AES.MODE_ECB)
        
        elif algorithm == Cypher.CBC.TYPE:
            plaintext  = Padding.appendPadding(plaintext, blocksize=Padding.AES_blocksize, mode=0)
            ciphertext = Cypher.CBC.encrypt(plaintext.encode(), key, AES.MODE_CBC, iv.encode())
        
        elif algorithm == Cypher.CTR.TYPE:
            plaintext  = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)
            ciphertext = Cypher.CTR.encrypt(plaintext.encode(), key, AES.MODE_CTR, iv.encode())
        
        elif algorithm == Cypher.Caesar.TYPE:
            ciphertext = Cypher.Caesar.encrypt(plaintext, password_caesar)
        
        elif algorithm == Cypher.OTP.TYPE:
            ciphertext = Cypher.OTP.encrypt(plaintext, password)
        
        elif algorithm == Cypher.Vigenere.TYPE:
            ciphertext = Cypher.Vigenere.encrypt(plaintext, password)
        
        msg = base64.b64encode(bytearray(ciphertext)).decode()

        if ChallengeCypher.APP.getDBController().addCypherChallenge(user.getUserID(), tip, msg, val, iv, msgHMAC, algorithm):
            crt.writeSuccess("Challenge submitted successfully!")
        else:
            crt.writeError("The challenge could not be submitted for unknown reasons.")
        crt.pause()


    @staticmethod
    def show(pause=True):
        """
        Lists every Cypher Challenge available

        Args:
            pause (bool, optional): if wished to be paused. Defaults to True.

        Returns:
            str: PrettyTable of every Cypher Challenge available
        """
        pt = ChallengeCypher.APP.getDBController().getAllCypherChallenges()
        crt.writeMessage(pt)
        if pause:
            crt.pause()
        return pt


    @staticmethod
    def choose(user : User, showall=True):
        """
        Awaits input for the Challenge wished to me solved 

        Args:
            user (User): User
            showall (bool, optional): True if wanted to list challenges. Defaults to True.
        """
        if showall:
            ChallengeCypher.show(user, pause=False)
        ChallengeCypher.solve(user, Read.tryAsInt("Choose challenge by ID: "))


    @staticmethod
    def solve(user : User, id_challenge):
        """
        Runs an attempt of user to solve the challenge

        Args:
            user (User): User
            id_challenge (int): ID of Challenge
        """
        challenge = ChallengeCypher.APP.getDBController().getCypherChallenge(id_challenge)
        if challenge is None:
            crt.writeError("This challenge does not exist.")
            crt.pause()
            return
        
        crt.writeMessage(f"Submitted by: {challenge['username']}")
        crt.writeMessage(f"Algorithm:    {challenge['algorithm']}")
        crt.writeMessage(f"Crypto:       {challenge['answer']}")
        crt.writeMessage(f"Plaintext:    {challenge['plaintext']}")
        crt.writeMessage(f"Tip:          {challenge['tip']}")
        crt.newLine()

        id_user = user.getUserID()

        last_try  = ChallengeCypher.APP.getDBController().getCypherLastTry(id_user, id_challenge)
        curr_time = Clock.now()
        if not (last_try is None or Clock.isAfter(curr_time, Clock.addSeconds(last_try, 15))):
            crt.writeWarning("Too soon to try again.")
            crt.pause()
            return None

        challenge['plaintext'] = Padding.appendPadding(challenge['plaintext'], blocksize=Padding.AES_blocksize, mode=0)

        if challenge['algorithm'] == Cypher.Caesar.TYPE:
            proposal_caesar = Read.tryAsInt("Insert your answer (number): ")
            proposal = str(proposal_caesar)
        else:
            proposal = Read.asString("Insert your answer: ")
        
        key      = hashlib.md5(proposal.encode()).digest()
        iv       = challenge['iv']
        hmacdb   = challenge['hmac']
        hmackey  = ChallengeCypher.APP.getDBController().getHMACKey()

        if challenge['algorithm'] == Cypher.ECB.TYPE:
            plaintext = Cypher.ECB.decrypt(base64.b64decode(challenge['answer']), key, AES.MODE_ECB)
        
        elif challenge['algorithm'] == Cypher.CBC.TYPE:
            plaintext = Cypher.CBC.decrypt(base64.b64decode(challenge['answer']), key, AES.MODE_CBC, iv.encode())
        
        elif challenge['algorithm'] == Cypher.CTR.TYPE:
            plaintext = Cypher.CTR.decrypt(base64.b64decode(challenge['answer']), key, AES.MODE_CTR, iv.encode())
        
        elif challenge['algorithm'] == Cypher.Caesar.TYPE:
            plaintext = Cypher.Caesar.decrypt(base64.b64decode(challenge['answer']), proposal_caesar)
        
        elif challenge['algorithm'] == Cypher.OTP.TYPE:
            plaintext = Cypher.OTP.decrypt(base64.b64decode(challenge['answer']), proposal)
        
        elif challenge['algorithm'] == Cypher.Vigenere.TYPE:
            plaintext = Cypher.Vigenere.decrypt(base64.b64decode(challenge['answer']), proposal)
        
        try:
            #plaintext = Padding.removePadding(plaintext.decode(),mode=0)
            plaintext = Padding.removePadding(plaintext, mode=0)
        except:
            ()
        msgHMAC = hmac.new(hmackey, plaintext.encode(), hashlib.sha256)

        # crt.writeDebug(f"{msgHMAC.hexdigest()} == {hmacdb}")
        if (msgHMAC.hexdigest() == hmacdb):
            if ChallengeCypher.APP.getDBController().updateCypherChallengeTry(id_user, id_challenge, Clock.now(), True):
                crt.writeSuccess("YOU DID IT!")
            else:
                crt.writeError("You got it, but I could not save the answer.")
        else:
            if ChallengeCypher.APP.getDBController().updateCypherChallengeTry(id_user, id_challenge, Clock.now(), False):
                crt.writeMessage("Better luck next time :(")
            else:
                crt.writeError("You did NOT got it, but I could not save the answer.")
        crt.pause()
