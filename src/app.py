import sys
from tui.menu import *
from tui.banner import BANNER
from dbhelper.dbcontrol import *
from login.user import *

class App(object):
    class flags:
        debug = False
        halt  = False


    def __init__(self):
        self.loadUI()
        self._db = DBControl()
        self._user = User(self._db)


    def debug(self, msg, end='\n'):
        if self.flags.debug:
            crt.writeDebug(f"Debug: {msg}", end=end)


    def launch(self, args=[]):
        if "--debug" in args or "-d" in args:
            self.flags.debug = True
        self._db.start()
        while not self.flags.halt:
            self._menuMain.exec()


    def finalize(self):
        crt.writeDebug("Stopping the app")
        exit(0)


    def userLogin(self):
        if self._user.login():
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
                MenuItem("AES-128-ECB", None),
                MenuItem("AES-128-CBC", None),
                MenuItem("AES-128-CTR", None),
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
                MenuItem("AES Cypher", None),
                MenuItem("Hash",       None),
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
            "Welcome User:",
            "HOMEPAGE",
            [
                MenuItem("List challenges",      Menu.exec_menu(self._menuListChallenges)),
                MenuItem("Submit new challenge", Menu.exec_menu(self._menuSubmitChallenge)),
                # MenuItem("Scoreboard",           None),
                # MenuItem("Settings",             None),
                MenuItem("Help",                 App.about),
                MenuItem("Logout",               None, isexit=True),
                MenuItem("QUIT",                 self.finalize)
            ]
        )

        self._menuMain = Menu(
            BANNER + "WELCOME",
            "Please choose an option to start with:",
            [
                MenuItem("Login",   self.userLogin),  # Menu.exec_menu(self._menuListChallenges)),
                MenuItem("Sign up", self.userSignup),  # Menu.exec_menu(self._menuSubmitChallenge)),
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
