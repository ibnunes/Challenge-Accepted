from Crypto.Cipher import AES
import hashlib
import Padding
import base64
import hmac
import secrets
# from prettytable import PrettyTable

# from app import App
from login.user import User
from utils.clock import Clock

"""
TODO: - Documentation
"""

from utils.crypto import Cypher
from utils.read import Read
from tui.cli import crt

class ChallengeCypher(object):
    APP = None

    @staticmethod
    def bindApp(app):
        ChallengeCypher.APP = app


    @staticmethod
    def add(user : User, algorithm):
        if not user.isLoggedIn():
            return False
        
        val      = Read.asString("Message: ")
        password = Read.asString("Cypher key: ")
        tip      = Read.asString("[Optional] Tip / Help: ")
        
        ival      = 10
        plaintext = val
        key       = hashlib.md5(password.encode()).digest()
        iv        = secrets.token_hex(8)    # hex(ival)[2:8].zfill(16)
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
            ciphertext = Cypher.CTR.encrypt(plaintext.encode(),key,AES.MODE_CTR,iv.encode())
        
        msg = base64.b64encode(bytearray(ciphertext)).decode()

        if ChallengeCypher.APP.getDBController().addCypherChallenge(user.getUserID(), tip, msg, val, iv, msgHMAC, algorithm):
            crt.writeSuccess("Challenge submitted successfully!")
        else:
            crt.writeError("The challenge could not be submitted for unknown reasons.")
        crt.pause()


    @staticmethod
    def show(pause=True):
        pt = ChallengeCypher.APP.getDBController().getAllCypherChallenges()
        crt.writeMessage(pt)
        if pause:
            crt.pause()
        return pt


    @staticmethod
    def choose(user : User, showall=True):
        if showall:
            ChallengeCypher.show(user, pause=False)
        ChallengeCypher.solve(user, Read.tryAsInt("Choose challenge by ID: "))


    @staticmethod
    def solve(user : User, id_challenge):
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

        #try:
        plaintext = Padding.removePadding(plaintext.decode(),mode=0)
        #except:
        #    ()
        msgHMAC = hmac.new(hmackey, plaintext.encode(), hashlib.sha256)

        crt.writeDebug(f"{msgHMAC.hexdigest()} == {hmacdb}")
        if (msgHMAC.hexdigest() == hmacdb):
            if ChallengeCypher.APP.getDBController().updateCypherChallengeTry(id_user, id_challenge, Clock.now(), True):
                crt.writeSuccess("YOU DID IT!")
            else:
                crt.writeError("You got it, but I could not save the answer.")
        else:
            ChallengeCypher.APP.getDBController().updateCypherChallengeTry(id_user, id_challenge, Clock.now(), False)
            crt.writeMessage("Better luck next time :(")
        crt.pause()