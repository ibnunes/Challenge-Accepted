from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
import binascii
import Padding
import base64
import mariadb
import os
from datetime import datetime, timedelta 
import time
#leitura do config.ini
import configparser

def decryptECB(ciphertext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.decrypt(ciphertext))

def decryptCBC(ciphertext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.decrypt(ciphertext))

def int_of_string(s):
    return int(binascii.hexlify(s), 16)

def decryptCTR(ciphertext,key, mode, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    encobj = AES.new(key,mode,counter=ctr)
    return(encobj.decrypt(ciphertext))


def responderDesafioCrypto(id_desafio_crypto, user):
    id_user = user #é preciso alterar para 
    config = configparser.ConfigParser()
    config.read(os.getcwd() + '/login/config.ini')
    #Ligação a BD
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
        
    try:
        conn2 = mariadb.connect(
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
        "SELECT desafios_cifras.resposta, desafios_cifras.dica, desafios_cifras.algoritmo, desafios_cifras.texto_limpo, utilizadores.username FROM desafios_cifras INNER JOIN utilizadores ON desafios_cifras.id_user=utilizadores.id_user WHERE id_desafio_cifras=?", 
        (id_desafio_crypto,))
    for (resposta, dica, algoritmo, texto_limpo, username) in cur:
        print("SUBMITTED BY: " + username)
        print("TIP: " + dica)
        print("ALGORITHM: " + algoritmo)
        print("PLAIN TEXT: " + texto_limpo)
        print("CRYPTO: " + resposta)
    
    texto_limpo = Padding.appendPadding(texto_limpo,blocksize=Padding.AES_blocksize,mode=0)
    print("INSERT YOUR ANSWER:")
    resp = input()
    key = hashlib.md5(resp.encode()).digest()

    if (algoritmo == 'ECB'):
        plaintext = decryptECB(base64.b64decode(resposta),key,AES.MODE_ECB)
        plaintext = Padding.removePadding(plaintext.decode(),mode=0)
        if (plaintext.strip() == texto_limpo.strip()):
            print("CONGRATULATIONS! YOU DID IT YOU LITTLE GENIUS!")
            return True
        else:
            print("YOU SHALL NOT PASS. WRONG ANSWER, TRY AGAIN!")
            return False
    if (algoritmo == 'CBC'):
        ival=10
        iv= hex(ival)[2:8].zfill(16)
        plaintext = decryptCBC(base64.b64decode(resposta),key,AES.MODE_CBC,iv.encode())
        plaintext = Padding.removePadding(plaintext.decode(),mode=0)
        if (plaintext.strip() == texto_limpo.strip()):
            print("CONGRATULATIONS! YOU DID IT YOU LITTLE GENIUS!")
            return True
        else:
            print("YOU SHALL NOT PASS. WRONG ANSWER, TRY AGAIN!")
            return False
    if(algoritmo == 'CTR'):
        ival=10
        iv= hex(ival)[2:8].zfill(16)
        plaintext = decryptCTR(base64.b64decode(resposta),key,AES.MODE_CTR,iv.encode())
        plaintext = Padding.removePadding(plaintext.decode(),mode=0)
        if (plaintext.strip() == texto_limpo.strip()):
            print("CONGRATULATIONS! YOU DID IT YOU LITTLE GENIUS!")
            return True
        else:
            print("YOU SHALL NOT PASS. WRONG ANSWER, TRY AGAIN!")
            return False
    