import sys

from challenge.cypher import ChallengeCypher
from tui.menu import *
from tui.banner import BANNER
from dbhelper.dbcontrol import *
from login.user import *
from utils.cypher import Cypher

class App(object):
    class flags:
        debug = False
        halt  = False


    def __init__(self):
        self.loadUI()
        self._db = DBControl()
        self._user = User(self._db)


    def getDBController(self):
        return self._db


    def debug(self, msg, end='\n'):
        if self.flags.debug:
            crt.writeDebug(f"Debug: {msg}", end=end)


    def launch(self, args=[]):
        if "--debug" in args or "-d" in args:
            self.flags.debug = True
        self._db.start()
        ChallengeCypher.bindApp(self)
        while not self.flags.halt:
            self._menuMain.exec()


    def finalize(self):
        self.debug("Stopping the app")
        exit(0)


    def userLogin(self):
        if self._user.login():
            self._menuHome.setSubtitle(f"Welcome {self._user.getUsername()}")
            self._menuHome.exec()
        else:
            crt.pause()


    def userSignup(self):
        if self._user.signup():
            crt.writeSuccess("New user registered.")
        crt.pause()


    def loadUI(self):
        self.debug("Loading UI...", end='')

        self._menuAddChallengeCypher = Menu(
            "Cypher Challenge",
            "Featuring AES",
            [
                MenuItem("AES-128-ECB", ChallengeCypher.add(self._user, Cypher.ECB.TYPE)),
                MenuItem("AES-128-CBC", ChallengeCypher.add(self._user, Cypher.CBC.TYPE)),
                MenuItem("AES-128-CTR", ChallengeCypher.add(self._user, Cypher.CTR.TYPE)),
                MenuItem("Back",        None, isexit=True),
                MenuItem("QUIT",        self.finalize)
            ]
        )

        self._menuAddHashChallenge = Menu(
            "Hash Challenge",
            "Featuring SHA and MD",
            [
                MenuItem("MD5",    None),
                MenuItem("SHA256", None),
                MenuItem("SHA512", None),
                MenuItem("Back",   None, isexit=True),
                MenuItem("QUIT",   self.finalize),
            ]
        )
        
        self._menuListChallenges = Menu(
            "CHALLENGES AVAILABLE",
            "",
            [
                MenuItem("AES Cypher: List all",         ChallengeCypher.show()),
                MenuItem("AES Cypher: Try to solve one", ChallengeCypher.choose(self._user, showall=False)),
                MenuItem("Hash: List all",               None),
                MenuItem("Hash: Try to solve one",       None),
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
        opt = self._menuYesNo.withTitle(prompt).exec()
        return True if opt == 0 else False


    @staticmethod
    def about():
        crt.writeMessage("ABOUT\n")
        crt.pause()



if __name__ == "__main__":
    try:
        app = App()
        app.launch(sys.argv)
    except Exception as ex:
        crt.writeFatal(f"FATAL: {ex}")
