import sys

from challenge.cypher import ChallengeCypher
from challenge.hash import ChallengeHash
from tui.menu import *
from tui.banner import BANNER
from dbhelper.dbcontrol import *
from login.user import *
from utils.cypher import Cypher, Hash

class App(object):
    class flags:
        """
        App flags
        
        Contains 2 states.
        - Debug (bool): Debug mode.
        - Halt (bool): When True App will be terminated.
        """
        debug = False
        halt  = False


    def __init__(self):
        """
        Initializes App by:
        - Loading the UI;
        - Initializing the Data Base Controller;
        - And the User class;
        """
        self._db = DBControl()          # TODO: separar DBControl do cliente
        self._user = User(self._db)
        self.loadUI()


    def getDBController(self):
        return self._db


    def debug(self, msg, end='\n'):
        """
        While in debug mode it prints to stdout.

        Args:
            msg (str): Message.
            end (str, optional): On what ends the message. Defaults to '\n'.
        """
        if self.flags.debug:
            crt.writeDebug(f"Debug: {msg}", end=end)


    def launch(self, args=[]):
        """
        Launches the App.

        Args:
            args (list, optional): System arguments passed on terminal. Defaults to [].
        """
        if "--debug" in args or "-d" in args:
            self.flags.debug = True
        self._db.start()
        ChallengeCypher.bindApp(self)
        ChallengeHash.bindApp(self)
        while not self.flags.halt:
            self._menuMain.exec()


    def finalize(self):
        """Finalizes the app, printing a debug message."""        
        self.debug("Stopping the app")
        exit(0)


    def userLogin(self):
        """On user login updates menuHome Subtitle to user's name."""        
        if self._user.login():
            self._menuHome.setSubtitle(f"Welcome {self._user.getUsername()}")
            self._menuHome.exec()
        else:
            crt.pause()


    def userSignup(self):
        """On a successful sign up presents user with a Success message."""        
        if self._user.signup():
            crt.writeSuccess("New user registered.")
        crt.pause()


    def loadUI(self):
        """Load each and every Menu. (Aka UI)"""        
        self.debug("Loading UI...", end='')

        self._menuAddChallengeCypher = Menu(
            "Cypher Challenge",
            "Featuring AES",
            [
                MenuItem("AES-128-ECB", lambda: ChallengeCypher.add(self._user, Cypher.ECB.TYPE)),
                MenuItem("AES-128-CBC", lambda: ChallengeCypher.add(self._user, Cypher.CBC.TYPE)),
                MenuItem("AES-128-CTR", lambda: ChallengeCypher.add(self._user, Cypher.CTR.TYPE)),
                MenuItem("Back",        None, isexit=True),
                MenuItem("QUIT",        self.finalize)
            ]
        )

        self._menuAddHashChallenge = Menu(
            "Hash Challenge",
            "Featuring SHA and MD",
            [
                MenuItem("MD5",    lambda: ChallengeHash.add(self._user, Hash.MD5.TYPE)),
                MenuItem("SHA256", lambda: ChallengeHash.add(self._user, Hash.SHA256.TYPE)),
                MenuItem("SHA512", lambda: ChallengeHash.add(self._user, Hash.SHA512.TYPE)),
                MenuItem("Back",   None, isexit=True),
                MenuItem("QUIT",   self.finalize),
            ]
        )
        
        self._menuListChallenges = Menu(
            "CHALLENGES AVAILABLE",
            "",
            [
                MenuItem("AES Cypher: List all",         ChallengeCypher.show),
                MenuItem("AES Cypher: Try to solve one", lambda: ChallengeCypher.choose(self._user, showall=False)),
                MenuItem("Hash: List all",               ChallengeHash.show),
                MenuItem("Hash: Try to solve one",       lambda: ChallengeHash.choose(self._user, showall=False)),
                MenuItem("Back",       None, isexit=True),
                MenuItem("QUIT",       self.finalize)
            ]
        )

        self._menuSubmitChallenge = Menu(
            "NEW CHALLENGE",
            "",
            [
                MenuItem("Decipher Challenge Type", Menu.exec_menu(self._menuAddChallengeCypher)), 
                MenuItem("Hash Challenge Type",     Menu.exec_menu(self._menuAddHashChallenge)), 
                MenuItem("Back",                    None, isexit=True),
                MenuItem("QUIT",                    self.finalize)
            ]
        )

        self._menuHome = Menu(
            "HOMEPAGE",
            "Welcome:",
            [
                MenuItem("List / solve challenges", Menu.exec_menu(self._menuListChallenges)),
                MenuItem("Submit new challenge",    Menu.exec_menu(self._menuSubmitChallenge)),
                # MenuItem("Scoreboard",              None),
                # MenuItem("Settings",                None),
                MenuItem("Help",                    App.about),
                MenuItem("Logout",                  None, isexit=True),
                MenuItem("QUIT",                    self.finalize)
            ]
        )

        self._menuMain = Menu(
            BANNER + "WELCOME",
            "Please choose an option to start with:",
            [
                MenuItem("Login",   self.userLogin),
                MenuItem("Sign up", self.userSignup),
                MenuItem("Help",    App.about),
                MenuItem("QUIT",    self.finalize, isexit=True)
            ]
        )

        self._menuYesNo = Menu(
            "", "",
            [
                MenuItem("Yes", None, isexit=True),
                MenuItem("No",  None, isexit=True)
            ]
        )

        self._menuBackQuit = Menu(
            "", "",
            [
                MenuItem("Back", None, isexit=True),
                MenuItem("QUIT", self.finalize)
            ]
        )

        self.debug("[OK]")


    def confirm(self, prompt=""):
        """
        Standard Menu for Yes or No decision.

        Args:
            prompt (str, optional): Stdout prompt. Defaults to "".

        Returns:
            bool: True when the option selected is Yes and False otherwise. 
        """        
        opt = self._menuYesNo.withTitle(prompt).exec()
        return opt == 0


    @staticmethod
    def about():
        """Content of About interface."""        
        crt.writeMessage("ABOUT\n")
        crt.pause()



if __name__ == "__main__":
    try:
        app = App()
        app.launch(sys.argv)
    except Exception as ex:
        crt.writeFatal(f"FATAL: {ex}")
