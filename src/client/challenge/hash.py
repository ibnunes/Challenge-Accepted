# from app import App
from login.user import User
from utils.crypto import Hash
from utils.read import Read
from tui.cli import crt
from utils.clock import Clock

class ChallengeHash(object):
    APP = None

    @staticmethod
    def bindApp(app):
        """
        Binds Challenge with the app.
    
        Args:
            app (App): Application
        """
        ChallengeHash.APP = app


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
        
        msg = Read.asString("Message: ").encode()
        tip = Read.asString("[Optional] Tip / Help: ")
        
        if algorithm == Hash.MD5.TYPE:
            msg = Hash.MD5.encrypt(msg)
        elif algorithm == Hash.SHA256.TYPE:
            msg = Hash.SHA256.encrypt(msg)
        elif algorithm == Hash.SHA512.TYPE:
            msg = Hash.SHA512.encrypt(msg)
        
        if ChallengeHash.APP.getDBController().addHashChallenge(user.getUserID(), tip, msg, algorithm):
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
        pt = ChallengeHash.APP.getDBController().getAllHashChallenges()
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
            ChallengeHash.show(user, pause=False)
        ChallengeHash.solve(user, Read.tryAsInt("Choose challenge by ID: "))


    @staticmethod
    def solve(user : User, id_challenge):
        """
        Runs an attempt of user to solve the challenge

        Args:
            user (User): User
            id_challenge (int): ID of Challenge
        """
        challenge = ChallengeHash.APP.getDBController().getHashChallenge(id_challenge)
        if challenge is None:
            crt.writeError("This challenge does not exist.")
            crt.pause()
            return
        
        crt.writeMessage(f"Submitted by: {challenge['username']}")
        crt.writeMessage(f"Algorithm:    {challenge['algorithm']}")
        crt.writeMessage(f"Hash:         {challenge['answer']}")
        crt.writeMessage(f"Tip:          {challenge['tip']}")
        crt.newLine()

        id_user = user.getUserID()

        last_try  = ChallengeHash.APP.getDBController().getHashLastTry(id_user, id_challenge)
        curr_time = Clock.now()
        if not (last_try is None or Clock.isAfter(curr_time, Clock.addSeconds(last_try, 15))):
            crt.writeWarning("Too soon to try again.")
            crt.pause()
            return None

        proposal = Read.asString("Insert your answer: ").encode()
        if challenge['algorithm'] == Hash.MD5.TYPE:
            proposal = Hash.MD5.encrypt(proposal)
        elif challenge['algorithm'] == Hash.SHA256.TYPE:
            proposal = Hash.SHA256.encrypt(proposal)
        elif challenge['algorithm'] == Hash.SHA512.TYPE:
            proposal = Hash.SHA512.encrypt(proposal)
        
        if proposal == challenge['answer']:
            if ChallengeHash.APP.getDBController().updateHashChallengeTry(id_user, id_challenge, Clock.now(), True):
                crt.writeSuccess("YOU DID IT!")
            else:
                crt.writeError("You got it, but I could not save the answer.")
        else:
            if ChallengeHash.APP.getDBController().updateHashChallengeTry(id_user, id_challenge, Clock.now(), False):
                crt.writeMessage("Better luck next time :(")
            else:
                crt.writeError("You did NOT got it, but I could not save the answer.")
        crt.pause()
