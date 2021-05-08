import hashlib
import os
import mariadb
import sys
import binascii

#leitura do config.ini
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
#fim leitura do config.ini

print("Registo de novo utilizador")
print("Username:")
username = input()
print("Email:")
email = input()
print("Password:")
password = input()


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
    exit()

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
print("Registo efectuado com sucesso - Let the challenges beggin!")
conn.close()