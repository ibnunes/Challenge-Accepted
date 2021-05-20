import hashlib
import mariadb
import binascii
import os
#Para esconder o input da password
from getpass import getpass

from dbhelper.dbcontrol import DBControl, UsernameNotFound, WrongPassword

#leitura do config.ini
import configparser


def loginUser():
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '/login/config.ini')
    #fim leitura do config.ini
    print ("Login Menu\n")
    print ("Insert Username:")
    input_username = input(" >>  ")
    print ("Insert Password:")
    input_password = getpass(" >>  ")
    password = ""
    salt = ""

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
        "SELECT id_user, password, salt FROM utilizadores WHERE username=?", 
        (input_username,))
    for (id_user, password, salt) in cur:
        salt = salt
        key = password
        id_user = id_user
    if (password != "" and salt != ""):
        new_key = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), binascii.unhexlify(salt), 100000)
        if new_key == binascii.unhexlify(key):
            return True
        else:
            print ("Senha errada")
            print("Tentar novamente?")
            a = input()
            return False
    else:
        print("Utilizador não encontrado")
        print("Tentar novamente?")
        a = input()
        return False