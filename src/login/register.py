import hashlib
import os
import mariadb
import sys
import binascii
from validate_email import validate_email
import re
#Para esconder o input da password
from getpass import getpass
#leitura do config.ini
import configparser

class SignUp(object):
    USER_REGEX = ()
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    
    def __init__(self) -> None:
        self._username = ""
        self._email = ""
        self._password = ""
        self._attempts = 3

    def validateUser(username) -> bool:
        
        pass
        
        
    def validateEmail(email) -> bool:
        return validate_email(
            email_address = email, 
            check_format = True, 
            check_blacklist = True, 
            check_dns = True, 
            dns_timeout = 10,
            check_smtp = True, 
            smtp_timeout = 10, 
            smtp_helo_host = 'my.host.name', 
            smtp_from_address = 'my@from.addr.ess', 
            smtp_debug = False
        )
        
    def checkPassword(password):
        """
        Verify the strength of 'password'
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
        errors = SignUp.checkPassword(password)
        tip = ""
        if errors["password_ok"]:
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
            
        return (errors["password_ok"], tip)
    

def registerUser():
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '/login/config.ini')
    #fim leitura do config.ini
    print ("Create Account Menu\n")
    print ("Insert New Email:")
    email = input(" >>  ")
    while(('@' not in email) or ('.' not in email)):
        print("Email is incorrect!!!")
        print ("Insert New Email:")
        email = input(" >>  ")
    print ("Insert New Username:")
    username = input(" >>  ")
    print ("Insert New Password:")
    password = getpass(" >>  ")
    print ("Confirm New Password:")
    passwordconf = getpass(" >>  ")
    while((password != passwordconf)):
        print ("Passwords don't match!!!")
        print ("Insert New Password:")
        password = getpass(" >>  ")
        print ("Confirm New Password:")
        passwordconf = getpass(" >>  ")
        
    # procura se existe o utilizador na base de dados
    try:
        conn = mariadb.connect(
            user=config['DATABASE']['user'],
            password=config['DATABASE']['password'],
            host=config['DATABASE']['host'],
            port=int(config['DATABASE']['port']),
            database=config['DATABASE']['database']

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    cur = conn.cursor()
    cur.execute(
        "SELECT username FROM utilizadores WHERE username=?", 
        (username,))
    for (user) in cur:
        print(f"O utilizador: {username} já está registado")
        registerUser()

    #Utilizador não existe na BD pode continuar

    #gera salt, calcula o sha256 (10000x) 
    salt = os.urandom(32) # A new salt for this user
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    #Grava na BD
    try: 
        cur.execute(
        "INSERT INTO utilizadores (username, email, password, salt) VALUES (?, ?, ?, ?)", 
        (username, email, binascii.hexlify(key), binascii.hexlify(salt)))
    except mariadb.Error as e: 
        print(f"Error: {e}")
    conn.commit() 
    conn.close()
    return True
