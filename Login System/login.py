import hashlib
import os
import mariadb
import sys
import binascii


print("Login")
print("Username:")
input_username = input() # The users username
print("Password:")
input_password = input() # The users password


# procura se existe o utilizador na base de dados
try:
    conn = mariadb.connect(
        user="cteam",
        password="w3KY3.EjFCMv5VBp",
        host="dlavareda.ddns.net",
        port=3300,
        database="cteam_projectosi"

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
    print('Password is correct')
else:
    print('Password is incorrect')