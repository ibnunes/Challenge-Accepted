import hashlib
import os
import mariadb
import sys
import binascii
#Para esconder o input da password
from getpass import getpass

#leitura do config.ini
import configparser

def loginUser():
    config = configparser.ConfigParser()
    config.read('src/login/config.ini')
    #fim leitura do config.ini
    print ("Login Menu\n")
    print ("Insert Username:")
    input_username = input(" >>  ")
    print ("Insert Password:")
    input_password = getpass(" >>  ")


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
        "SELECT password, salt FROM utilizadores WHERE username=?", 
        (input_username,))
    for (password, salt) in cur:
        salt = salt
        key = password


    new_key = hashlib.pbkdf2_hmac('sha256', input_password.encode('utf-8'), binascii.unhexlify(salt), 100000)


    if new_key == binascii.unhexlify(key):
        return True
    else:
        return False