import re
from dbhelper.dbcontrol import *
from utils.read         import Read
from tui.cli            import crt
from validate_email     import validate_email


class User(object):
    NO_USER = -1

    def __init__(self, dbcontroller : DBControl):
        """
        Initializes User.

        Args:
            dbcontroller (DBControl): Data Base Controller.
        """        
        self._username  = ""
        self._password  = ""
        self._email     = ""
        self._dbcontrol = dbcontroller
        self._logged    = False
        self._userid    = User.NO_USER
        self._cyphercreated = 0
        self._hashcreated   = 0
        self._totalcreated  = 0
        self._tried     = 0
        self._solved    = 0


    def __str__(self) -> str:
        self.updateProfile()
        
        return \
        f"          Username : {self._username}\n"        \
        f"             Email : {self._email}\n"           \
        f"Created Challenges : {self._created}\n"         \
        f"          (Cypher) : {self._cyphercreated}\n"   \
        f"            (Hash) : {self._hashcreated}\n"     \
        f"  Tried Challenges : {self._tried}\n"           \
        f" Solved Challenges : {self._solved}\n"          \
        
        
    def updateProfile(self):
        amount = self._dbcontrol.getUserCreatedAmount(self._userid)
        self._cyphercreated = amount['cypher']
        self._hashcreated = amount['hash']
        self._created = amount['total']

    def wipe(self):
        """Resets User stats."""        
        self._username = ""
        self._password = ""


    def getUsername(self):
        """
        Returns:
            str: Username of the User.
        """        
        return self._username
    
    def getEmail(self):
        return self._email


    def getUserID(self):
        """
        Returns:
            int: UserID of User.
        """
        return self._userid


    def getSolved(self):
        """
            Gets the number of solved challenges.

            Returns:
                int: Solved Challengess
        """
        return self._solved


    def isLoggedIn(self):
        """
        Returns:
            bool: True if user is logged False otherwise.
        """        
        return self._logged


    def logout(self):
        """Logs User out."""        
        self.wipe()
        self._logged = False
        self._userid = User.NO_USER


    def login(self):
        """
        Logs User in.

        Returns:
            bool: True if successfully logged in False otherwise.
        """        
        self._username = Read.asString("Username: ")
        self._password = Read.asPassword("Password: ")
        try:
            (ok, id_user) = self._dbcontrol.loginUser(self._username, self._password)
            if ok:
                self._logged = True
                self._userid = id_user
                self._email  = self._dbcontrol.getEmail(id_user)
        except (UsernameNotFound, WrongPassword) as ex:
            crt.writeWarning(ex.message)
            self._logged = False
            self.wipe()
        return self._logged


    def signup(self):
        """
        Signs up User.

        Returns:
            bool: True if successfully registered False otherwise.
        """
        while True:
            username = Read.asString("New username: ")
            isValid, tip = User.validateUsername(username)
            if not isValid:
                crt.writeWarning(tip)
            elif self._dbcontrol.userExists(username):
                crt.writeWarning(f"User '{username}' already exists.")
            else:
                break

        while True:
            email = Read.asString("Email: ")
            if not User.validateEmail(email):
                crt.writeWarning(f"Email '{email}' not valid.")
            elif self._dbcontrol.emailExists(email):
                crt.writeWarning(f"Email '{email}' already in use.")
            else:
                break
                
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

    
    def checkUsername(username):
        """
        Checks the validity of 'username'
        A username is considered valid when:
            - 3 characters length or more
            - Its characters are fully ASCII

        Args:
            username (str): Given username to validate.

        Returns:
            dict: Indicates the wrong criteria
        """        
        length_error = len(username) < 3
        
        ascii_error = not (username == (username.encode().decode(
            'ascii', 'replace').replace(u'\ufffd', '_')))
        
        username_ok = not (length_error or ascii_error)
        
        return {
            'username_ok': username_ok,
            'length_error': length_error,
            'ascii_error': ascii_error
        }


    def validateUsername(username) -> tuple:
        """
        Declares if a given username is valid or not.

        Args:
            password (str): Given username to validate.

        Returns:
            tuple: (isValid, tip)
                `isValid` (bool): True if `username` is validated
                `tip` (str): Explanation on what is preventing `password` to be validated.
        """
        errors = User.checkUsername(username)
        isValid = errors['username_ok']
        tip = ""
        
        if not isValid:
            if errors['length_error']:
                tip += "Your username is too short. It must have at least 3 characters.\n"
            
            if errors['ascii_error']:
                tip += "Your username has invalid characters. Please try again with a new one.\n"

        return isValid, tip


    def validateEmail(email) -> bool:
        """
        Validates `email`

        Args:
            email (str): Given email to validate.

        Returns:
            bool: True or False depending if the email address exists or/and can be delivered.
            None: If the result is ambigious.
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


    def checkPassword(password) -> dict:
        """
        Checks the strength of 'password'
        A password is considered strong when:
            8 characters length or more
            Its characters are fully ASCII
            1 digit or more
            1 symbol or more
            1 uppercase letter or more
            1 lowercase letter or more
        
        Args:
            password (str): Given password

        Returns:
            dict: Indicates the wrong criteria
        """
        
        # Calculating the length
        length_error = len(password) < 8
        
        # Are there illegal characters?
        ascii_error = not (password == (password.encode().decode(
            'ascii', 'replace').replace(u'\ufffd', '_')))

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
            length_error or ascii_error or digit_error or uppercase_error or lowercase_error or symbol_error
        )

        return {
            'password_ok': password_ok,
            'length_error': length_error,
            'ascii_error': ascii_error,
            'digit_error': digit_error,
            'uppercase_error': uppercase_error,
            'lowercase_error': lowercase_error,
            'symbol_error': symbol_error
        }
        

    def validatePassword(password) -> tuple:
        """
        Declares if a given password is valid or not.

        Args:
            password (str): Password you wish to validate.

        Returns:
            tuple: (isValid, tip)
                `isValid` (bool): True if `password` is validated
                `tip` (str): Explanation on what is preventing `password` to be validated.
        """
        
        errors = User.checkPassword(password)
        isValid = errors["password_ok"]
        tip = ""
        
        if not isValid:
            if errors['length_error']:
                tip += "Your Password is too short. It must contain at least 8 characters.\n"

            if errors['ascii_error']:
                tip += "Your username has invalid characters. Please try again with ASCII characters.\n"
                
            if errors['digit_error']:
                tip += "Your Password should contain at least 1 number. (0-9)\n"

            if errors['uppercase_error']:
                tip += "Your Password should contain at least 1 uppercase character. (A-Z)\n"

            if errors['lowercase_error']:
                tip += "Your Password should contain at least 1 lowercase character. (a-z)\n"

            if errors['symbol_error']:
                tip += "Your Password should contain at least 1 symbol.\n"
                
        return isValid, tip
