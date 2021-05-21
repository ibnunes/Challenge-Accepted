import secrets
from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
import binascii
import Padding
import base64
import mariadb
import time
import os
import hmac
import secrets
from sympy.crypto.crypto import encipher_vigenere
from sympy.crypto.crypto import decipher_vigenere
from elgamal.elgamal import Elgamal
import pycaesarcipher
import onetimepad


#leitura do config.ini
import configparser
config = configparser.ConfigParser()
config.read(os.getcwd() + '/login/config.ini')

#fim leitura do config.ini


def encryptECB(plaintext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.encrypt(plaintext))

def decryptECB(ciphertext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.decrypt(ciphertext))

def encryptCBC(plaintext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.encrypt(plaintext))

def decryptCBC(ciphertext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.decrypt(ciphertext))

def int_of_string(s):
    return int(binascii.hexlify(s), 16)

def encryptCTR(plaintext,key, mode, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    encobj = AES.new(key,mode,counter=ctr)
    return(encobj.encrypt(plaintext))

def decryptCTR(ciphertext,key, mode, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    encobj = AES.new(key,mode,counter=ctr)
    return(encobj.decrypt(ciphertext))

def encryptOTP(plaintext, key):
    encobj = onetimepad.encrypt(plaintext, key)
    return(encobj)

def decryptOTP(ciphertext, key):
    encobj = onetimepad.decrypt(ciphertext, key)
    return(encobj.decrypt(ciphertext))

def encryptVigenere(plaintext, key):
    encobj = encipher_vigenere(plaintext, key)
    return(encobj)

def decryptVigenere(ciphertext, key):
    encobj = decipher_vigenere(ciphertext, key)
    return(encobj.decrypt(ciphertext))

def encryptCaesar(plaintext, key):
    word = pycaesarcipher.pycaesarcipher()
    encobj = word.caesar_encipher(plaintext, key)
    return(encobj.encode())

def decryptCaesar(ciphertext, key, word):
    encobj = word.caesar_decripher(ciphertext, key)
    return(encobj.decrypt(ciphertext))

def encryptElgamal(plaintext, key):
    encobj = Elgamal.encrypt(plaintext, key)
    return(encobj)

def decryptElgamal(ciphertext, key):
    encobj = Elgamal.decrypt(ciphertext, key)
    return(encobj.decrypt(ciphertext, key))


def adicionarDesafioCypher(user):
    id_user = user
    print("AES CYPHER CHALLENGE\n")
    print("1. AES-128-ECB ALGORITHM")
    print("2. AES-128-CBC ALGORITHM")
    print("3. AES-128-CTR ALGORITHM")
    print("9. Back")
    print("0. Quit")
    algoritmo = input()
    if (algoritmo != "0" and algoritmo != "9"):
        print("Message:")
        val = input()
        print("Cypher Key:")
        password = input()
        print ("If you want, leave a tip for the users who will try to answer this challenge:")
        dica = input()
        ival=10
        
        plaintext=val
        #Gerar um hash de 128bits pra uso como key no AES
        #Derivação da password
        key = hashlib.md5(password.encode()).digest()
        iv = secrets.token_hex(8)
        #criação do HMAC para gravar na BD
        keyHMAC = b'secret'
        msgHMAC = hmac.new(keyHMAC, val.encode(), hashlib.sha256)

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

    cur = conn.cursor()

    #ECB
    if (algoritmo == "1"):
        
        plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

        ciphertext = encryptECB(plaintext.encode(),key,AES.MODE_ECB)
        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext)).decode()

        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo) VALUES (?, ?, ?, ?, ?, ?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), 'ECB'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    #CBC
    if (algoritmo == "2"):
        
        plaintext=val
        plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

        ciphertext = encryptCBC(plaintext.encode(),key,AES.MODE_CBC,iv.encode())
        
        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext)).decode()

        #Grava na BD

        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo, iv) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), 'CBC', iv))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    #CTR
    if (algoritmo == "3"):
        
        plaintext=val
        plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

        ciphertext = encryptCTR(plaintext.encode(),key,AES.MODE_CTR,iv.encode())
        
        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext)).decode()
        
        #Grava na BD
        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo, iv) VALUES (?, ?, ?, ?, ?, ?,?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), 'CTR', iv))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1
    
    if (algoritmo == "9"):
        return 9
    if (algoritmo == "0"):
        return 0
    
def adicionarDesafioCypher2(user):
    id_user = user
    print("OTHER CHALLENGES\n")
    print("1. CAESAR CYPHER")
    print("2. ELGAMAL")
    print("3. ONE-TIME-PAD")
    print("4. VIGINERE CYPHER")
    print("9. Back")
    print("0. Quit")
    algoritmo = input()
    if (algoritmo != "0" and algoritmo != "9" and algoritmo != "2"):
        print("Message:")
        val = input()
        print("Cypher Key:")
        password = input()
        print ("If you want, leave a tip for the users who will try to answer this challenge:")
        dica = input()
        ival=10
        
        plaintext=val
        #Gerar um hash de 128bits pra uso como key no AES
        #Derivação da password
        key = hashlib.md5(password.encode()).digest()

        iv= hex(ival)[2:8].zfill(16)
        #criação do HMAC para gravar na BD
        keyHMAC = b'secret'
        msgHMAC = hmac.new(keyHMAC, val.encode(), hashlib.sha256)

    #para caesar e elgamal
    if (algoritmo == "2"):
        print("Message:")
        val = input()
        print ("If you want, leave a tip for the users who will try to answer this challenge:")
        dica = input()
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

    cur = conn.cursor()

    #CAESAR
    if (algoritmo == "1"):
        if(password.isdigit()):
            plaintext = val
            ciphertext = encryptCaesar(val, int(password))
            #String a guardar na BD
            msg = base64.b64encode(ciphertext)

            try: 
                cur.execute(
                "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo) VALUES (?, ?, ?, ?, ?, ?)", 
                (id_user, dica, msg, val, msgHMAC.hexdigest(), 'CAESAR'))
            except mariadb.Error as e: 
                print(f"Error: {e}")
            conn.commit()
            print("Your challenge was submitted - Let the challenges begin!")
            conn.close()
        else:
            print("Input is not digit!")
        return 1

    #ELGAMAL
    if (algoritmo == "2"):
        
        plaintext = val
        pb, pv = Elgamal.newkeys(6)
        pKey = "" + str(pv.p) + str(pv.x)
        
        ciphertext = encryptElgamal(plaintext.encode(), pb)
        
        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext)).decode()
    
        #Grava na BD

        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, iv, algoritmo) VALUES (?, ?, ?, ?, ?, ?, ?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), pKey, 'ELGAMAL'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    #ONETIMEPAD
    if (algoritmo == "3"):
        
        while (len(val)!= len(password)):
            print("Chave de Cifra tem que ter o mesmo tamanho que a mensagem a cifrar!")
            print("Chave de cifra")
            password = input()
        
        plaintext = val

        ciphertext = encryptOTP(plaintext, password)

        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext.encode()))
        
        #Grava na BD
        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo) VALUES (?, ?, ?, ?, ?, ?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), 'ONETIMEPAD'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1
    #VIGENERE
    if (algoritmo == "4"):
        
        plaintext=val

        ciphertext = encryptVigenere(plaintext, password)
        
        #String a guardar na BD
        msg = base64.b64encode(bytearray(ciphertext.encode()))
        
        
        #Grava na BD
        try: 
            cur.execute(
            "INSERT INTO desafios_cifras (id_user, dica, resposta, texto_limpo, hmac, algoritmo) VALUES (?, ?, ?, ?, ?, ?)", 
            (id_user, dica, msg, val, msgHMAC.hexdigest(), 'VIGENERE'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    if (algoritmo == "9"):
        return 9
    if (algoritmo == "0"):
        return 0