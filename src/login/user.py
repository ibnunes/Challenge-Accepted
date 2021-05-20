from dbhelper.dbcontrol import *
from utils.read         import Read
from tui.cli            import crt


class User(object):
    def __init__(self, dbcontroller : DBControl):
        self._username  = ""
        self._password  = ""
        self._dbcontrol = dbcontroller
        self._logged    = False


    def wipe(self):
        self._username = ""
        self._password = ""
        self._logged   = False


    def logout(self):
        self.wipe()


    def login(self):
        self._username = Read.asString("Username: ")
        self._password = Read.asPassword("Password: ")
        try:
            if self._dbcontrol.loginUser(self._username, self._password):
                self._logged = True
        except (UsernameNotFound, WrongPassword) as ex:
            crt.writeWarning(ex.message)
            self._logged = False
            self.wipe()
        return self._logged


    def signup(self):
        email = Read.asString("Email: ")
        # TODO: validar Email
        while True:
            username = Read.asString("New username: ")
            if self._dbcontrol.userExists(username):
                crt.writeWarning(f"User '{username} already exists.")
            else:
                break
        while True:
            password = Read.asPassword("Password: ")
            password_check = Read.asPassword("Repeat password: ")
            if password != password_check:
                crt.writeWarning("Passwords do not coincide.")
            else:
                break
        return self._dbcontrol.registerUser(username, password, email)
