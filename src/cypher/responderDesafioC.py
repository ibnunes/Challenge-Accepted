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
import codecs
import hmac
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
        "SELECT desafios_cifras.resposta, desafios_cifras.dica, desafios_cifras.algoritmo, desafios_cifras.texto_limpo, desafios_cifras.hmac, utilizadores.username FROM desafios_cifras INNER JOIN utilizadores ON desafios_cifras.id_user=utilizadores.id_user WHERE id_desafio_cifras=?", 
        (id_desafio_crypto,))
    for (resposta, dica, algoritmo, texto_limpo, hmacDB, username) in cur:
        print("SUBMITTED BY: " + username)
        print("TIP: " + dica)
        print("ALGORITHM: " + algoritmo)
        print("PLAIN TEXT: " + texto_limpo)
        print("CRYPTO: " + resposta)
    
    print("INSERT YOUR ANSWER:")
    resp = input()
    key = hashlib.md5(resp.encode()).digest()
    keyHMAC = b'secret'
    

    if (algoritmo == 'ECB'):
        plaintext = decryptECB(base64.b64decode(resposta),key,AES.MODE_ECB)
        plaintext2 = codecs.decode(plaintext, encoding='utf-8', errors='ignore')
        try:
            plaintext2 = Padding.removePadding(plaintext2,mode=0)
        except Exception:
            ()
        msgHMAC = hmac.new(keyHMAC, plaintext2.encode(), hashlib.sha256)
    if (algoritmo == 'CBC'):
        ival=10
        iv= hex(ival)[2:8].zfill(16)
        plaintext = decryptCBC(base64.b64decode(resposta),key,AES.MODE_CBC,iv.encode())
        try:
            plaintext2 = Padding.removePadding(plaintext2,mode=0)
        except Exception:
            ()
    if(algoritmo == 'CTR'):
        ival=10
        iv= hex(ival)[2:8].zfill(16)
        plaintext = decryptCTR(base64.b64decode(resposta),key,AES.MODE_CTR,iv.encode())
        try:
            plaintext2 = Padding.removePadding(plaintext2,mode=0)
        except Exception:
            ()
            
    if (msgHMAC.hexdigest() == hmacDB):
        # Verifica a hora da ultima submissão desde utilizador a este desafio
        cur2 = conn.cursor()
        cur2.execute(
            "SELECT data_ultima_tentativa FROM utilizadores_cifras WHERE id_user=? AND id_desafio_cifras = ? ORDER BY data_ultima_tentativa DESC LIMIT 1", 
            (id_user, id_desafio_crypto))
        
        #Para os casos em que ja existe uma tentativa deste utilizador neste desafio
        for (data_ultima_tentativa) in cur2:
            new_date = data_ultima_tentativa[0] + 15
            tempoactual = int(time.time())
            if(new_date > tempoactual):
                print("Take it easy, you gotta wait a bit longer to submit another answer.")
                conn.close()
                conn2.close()
                return
            else:
                #Pode inserir
                #Insere a resolução
                #Grava na BD
                try: 
                    cur3 = conn2.cursor()
                    cur3.execute(
                    "INSERT INTO utilizadores_cifras (id_user, id_desafio_cifras, data_ultima_tentativa, sucesso) VALUES (?, ?, ?, ?)", 
                    (id_user, id_desafio_crypto, int(time.time()), True))
                    conn2.commit() 
                except mariadb.Error as e: 
                    print(f"Error: {e}")
                conn.close()
                conn2.close()
                print("CONGRATULATIONS! YOU DID IT!")
                print("                                           .''.      ")
                print("       .''.      .        *''*    :_\/_:     .       ")
                print("      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.    ")
                print("  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-    ")
                print(" :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'    ")
                print(" : /\ : :::::     *_\/_*     -= o =-  /)\    '  *    ")
                print("  '..'  ':::'     * /\ *     .'/.\'.   '             ")
                print("      *            *..*         :                    ")
                print("       *                                             ")
                print("        *                                            ")
                return True #Como ja inseriu fecha

        #Para os casos em que não existe uma tentativa deste utilizador neste desafio
            #Pode inserir
            #Insere a resolução
            #Grava na BD
        cursor = cur2.fetchall()
        date = len(cursor)
        if(date == 0):
            try: 
                cur3 = conn2.cursor()
                cur3.execute(
                "INSERT INTO utilizadores_cifras (id_user, id_desafio_cifras, data_ultima_tentativa, sucesso) VALUES (?, ?, ?, ?)", 
                (id_user, id_desafio_crypto, int(time.time()), True))
                conn2.commit() 
            except mariadb.Error as e: 
                print(f"Error: {e}")
            conn.close()
            conn2.close()
            print("CONGRATULATIONS! YOU DID IT!")
            print("                                           .''.      ")
            print("       .''.      .        *''*    :_\/_:     .       ")
            print("      :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.    ")
            print("  .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-    ")
            print(" :_\/_:'.:::.    ' *''*    * '.\'/.' _\(/_'.':'.'    ")
            print(" : /\ : :::::     *_\/_*     -= o =-  /)\    '  *    ")
            print("  '..'  ':::'     * /\ *     .'/.\'.   '             ")
            print("      *            *..*         :                    ")
            print("       *                                             ")
            print("        *                                            ")
            return True
    else:
        try: 
            cur3 = conn2.cursor()
            cur3.execute(
            "INSERT INTO utilizadores_cifras (id_user, id_desafio_cifras, data_ultima_tentativa, sucesso) VALUES (?, ?, ?, ?)", 
            (id_user, id_desafio_crypto, int(time.time()), False))
            conn2.commit() 
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.close()
        conn2.close()
        print("YOU SHALL NOT PASS. WRONG ANSWER, TRY AGAIN!")
        print("""    .-''''''-.
  .'          '.
 /   O      O   \\
:           `    :
|                | 
:    .------.    :
 \  '        '  /
  '.          .'
    '-......-'""")
        return False