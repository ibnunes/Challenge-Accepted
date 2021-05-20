import re
from dbhelper.dbcontrol import *
from utils.read         import Read
from tui.cli            import crt
from validate_email import validate_email


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


    def getUsername(self):
        return self._username


    def isLoggedIn(self):
        return self._logged


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
        while True:
            username = Read.asString("New username: ")
            if self._dbcontrol.userExists(username):
                crt.writeWarning(f"User '{username} already exists.")
            else:
                break

        while True:
            email = Read.asString("Email: ")
            if User.validateEmail(email):
                break
            else:
                crt.writeWarning(f"Email '{email}' not valid.")

        while True:
            password = Read.asPassword("Password: ")
            isValid, tip = User.validatePassword(password)
            if not isValid:
                crt.writeWarning(tip)
            else:
                password_check = Read.asPassword("Repeat password: ")
                if password != password_check:
                    crt.writeWarning("Passwords do not coincide.")
                else:
                    crt.writeSuccess(tip)
                    break
            
        return self._dbcontrol.registerUser(username, password, email)


    def validateEmail(email) -> bool:
        """
        Validates `email`
        
        Return True or False depending if the email address exists or/and can be delivered.
        Return None if the result is ambigious.
        """
        return validate_email(
            email_address=email,
            check_format=True,
            check_blacklist=True,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_timeout=10,
            smtp_helo_host='my.host.name',
            smtp_from_address='my@from.addr.ess',
            smtp_debug=False
        )


    def checkPassword(password):
        """
        Checks the strength of 'password'
        
        Returns a dict indicating the wrong criteria
        A password is considered strong if:
            8 characters length or more
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        """

        # Calculating the length
        length_error = len(password) < 8

        # Searching for digits
        digit_error = re.search(r"\d", password) is None

        # Searching for uppercase
        uppercase_error = re.search(r"[A-Z]", password) is None

        # Searching for lowercase
        lowercase_error = re.search(r"[a-z]", password) is None

        # Searching for symbols
        symbol_error = re.search(r"\W", password) is None

        # Overall result
        password_ok = not (
            length_error or digit_error or uppercase_error or lowercase_error or symbol_error
        )

        return {
            'password_ok': password_ok,
            'length_error': length_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'symbol_error': symbol_error
        }
        

    def validatePassword(password) -> tuple(bool, str):
        errors = User.checkPassword(password)
        isStrong = errors["password_ok"]
        tip = ""
        
        if isStrong:
            tip = "Your Password is strong!\n"
        else:
            if errors["length_error"]:
                tip += "Your Password is too short. It must contain at least 8 characters.\n"

            if errors["digit_error"]:
                tip += "Your Password should contain at least 1 number. (0-9)\n"

            if errors["uppercase_error"]:
                tip += "Your Password should contain at least 1 uppercase character. (A-Z)\n"

            if errors["lowercase_error"]:
                tip += "Your Password should contain at least 1 lowercase character. (a-z)\n"

            if errors["symbol_error"]:
                tip += "Your Password should contain at least 1 symbol.\n"

        return (isStrong, tip)
