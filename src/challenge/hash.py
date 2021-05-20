# from app import App
from login.user import User

from utils.cypher import Hash
from utils.read import Read
from tui.cli import crt

class ChallengeHash(object):
    APP = None

    @staticmethod
    def bindApp(app):
        ChallengeHash.APP = app


    @staticmethod
    def add(user : User, algorithm):
        if not user.isLoggedIn():
            return False
        
        msg = Read.asString("Message: ").encode()
        tip = Read.asString("[Optional] Tip / Help: ")
        
        if ChallengeHash.APP.getDBController().addHashChallenge(user.getUserID(), tip, msg, algorithm):
            crt.writeSuccess("Challenge submitted successfully!")
        else:
            crt.writeError("The challenge could not be submitted for unknown reasons.")
        crt.pause()


    @staticmethod
    def show(pause=True):
        pt = ChallengeHash.APP.getDBController().getAllHashChallenges()
        crt.writeMessage(pt)
        if pause:
            crt.pause()
        return pt


    @staticmethod
    def choose(user : User, showall=True):
        if showall:
            ChallengeHash.show(user, pause=False)
        ChallengeHash.solve(Read.tryAsInt("Choose challenge by ID: "))


    @staticmethod
    def solve(user : User, id_challenge):
        pass