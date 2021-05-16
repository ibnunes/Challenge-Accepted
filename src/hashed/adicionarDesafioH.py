import mariadb
from Crypto.Hash import SHA256, SHA512, MD5
#leitura do config.ini
import configparser
config = configparser.ConfigParser()
config.read('/home/btc/Documents/Challenge-Accepted/src/login/config.ini')

#fim leitura do config.ini

id_user = 27 #é preciso alterar para 

def adicionarDesafioHash():
    print("HASH CHALLENGE\n")
    print("1. MD5 ALGORITHM")
    print("2. SHA256 ALGORITHM")
    print("3. SHA512 ALGORITHM")
    print("9. Back")
    print("0. Quit")
    algoritmo = input()
    if (algoritmo != "0" and algoritmo != "9"):
        print ("Message:")
        msg = input().encode()
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

    #MD5
    if (algoritmo == "1"):
        h = MD5.new()
        h.update(msg)
        #Grava na BD

        try: 
            cur.execute(
            "INSERT INTO desafios_hash (id_user, dica, resposta, algoritmo) VALUES (?, ?, ?, ?)", 
            (id_user, dica, h.hexdigest(), 'MD5'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    if (algoritmo == "2"):
        h = SHA256.new()
        h.update(msg)
        #Grava na BD

        try: 
            cur.execute(
            "INSERT INTO desafios_hash (id_user, dica, resposta, algoritmo) VALUES (?, ?, ?, ?)", 
            (id_user, dica, h.hexdigest(), 'SHA256'))
        except mariadb.Error as e: 
            print(f"Error: {e}")
        conn.commit() 
        print("Your challenge was submitted - Let the challenges begin!")
        conn.close()
        return 1

    if (algoritmo == "3"):
        h = SHA512.new()
        h.update(msg)
        #Grava na BD
        try: 
            cur.execute(
            "INSERT INTO desafios_hash (id_user, dica, resposta, algoritmo) VALUES (?, ?, ?, ?)", 
            (id_user, dica, h.hexdigest(), 'SHA512'))
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