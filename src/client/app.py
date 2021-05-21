import sys, os
import configparser as ini

from challenge.cypher import ChallengeCypher
from challenge.hash import ChallengeHash
from tui.menu import *
from tui.banner import BANNER
from dbhelper.dbcontrol import *
from login.user import *
from utils.crypto import Cypher, Hash

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
        self._config = ini.ConfigParser()
        self._config.read(os.getcwd() + '/config.ini')
        self._db = DBControl()
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
        self._db.start(
            url=self._config['SERVER']['host'],
            port=self._config['SERVER']['port']
        )
        ChallengeCypher.bindApp(self)
        ChallengeHash.bindApp(self)
        while not self.flags.halt:
            self._menuMain.exec()


    def finalize(self):
        """Finalizes the app, printing a debug message."""        
        self.debug("Stopping the app")
        self._db.stop()
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
                MenuItem("Scoreboard",              lambda: User.showScoreboard(self)),
                # MenuItem("Settings",                None),
                MenuItem("Profile",                 lambda: App.profile(self._user)),
                MenuItem("Help",                    App.about),
                MenuItem("Logout",                  None, isexit=True),
                MenuItem("QUIT",                    self.finalize)
            ]
        )

        self._menuMain = Menu(
            BANNER + "\n\nWELCOME",
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
        crt.clearScreen()
        crt.writeMessage(
f"""{BANNER}

Encryption contains excellent tools for developing challenging mystery games.
The idea of this work is to develop a system that allows different users to publish and solve challenges.

    Igor Nunes          github.com/thoga31
    Diogo Simões        github.com/AshKetshup
    Diogo Lavareda      github.com/dlavareda
    Beatriz Costa       github.com/beatriztcosta
    Joana Almeida       github.com/joanalmeida99

UBI - University of Beira Interior, Portugal


    Build:              1.0.0-beta
    Date:               May 2021
    License:            GNU-GPL 3.0
"""
        )
        crt.pause()


    def profile(user):
        """Content of User profile"""        
        crt.writeMessage("PROFILE\n")
        crt.writeMessage(str(user))
        crt.pause()


if __name__ == "__main__":
    try:
        app = App()
        app.launch(sys.argv)
    except Exception as ex:
        crt.writeFatal(f"FATAL: {ex}")
