import mariadb
from Crypto.Hash import SHA256, SHA512, MD5
from datetime import datetime, timedelta 
import time
import os
#leitura do config.ini
import configparser

def responderDesafioHash(id_desafio_hash):
    id_user = 27 #é preciso alterar para 
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
        "SELECT desafios_hash.resposta, desafios_hash.dica, desafios_hash.algoritmo, utilizadores.username FROM desafios_hash INNER JOIN utilizadores ON desafios_hash.id_user=utilizadores.id_user WHERE id_desafio_hash=?", 
        (id_desafio_hash,))
    for (resposta, dica, algoritmo, username) in cur:
        print("SUBMITTED BY: " + username)
        print("TIP: " + dica)
        print("ALGORITHM: " + algoritmo)
        print("HASH: " + resposta)

    print("INSERT YOUR ANSWER:")
    resp = input().encode()
    if (algoritmo == 'MD5'):
        h = MD5.new()
        h.update(resp)
    if (algoritmo == 'SHA256'):
        h = SHA256.new()
        h.update(resp)
    if(algoritmo == 'SHA512'):
        h = SHA512.new()
        h.update(resp)

    if (h.hexdigest() == resposta):
        # Verifica a hora da ultima submissão desde utilizador a este desafio
        cur2 = conn.cursor()
        cur2.execute(
            "SELECT data_ultima_tentativa FROM utilizadores_hash WHERE id_user=? AND id_desafio_hash = ? ORDER BY data_ultima_tentativa DESC LIMIT 1", 
            (id_user, id_desafio_hash))  
        #Para os casos em que ja existe uma tentativa deste utilizador neste desafio
        for (data_ultima_tentativa) in cur2:
            new_date = data_ultima_tentativa[0] + 15
            tempoactual = int(time.time())
            if(new_date > tempoactual):
                print("Espere mais tempo")
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
                    "INSERT INTO utilizadores_hash (id_user, id_desafio_hash, data_ultima_tentativa, sucesso) VALUES (?, ?, ?, ?)", 
                    (id_user, id_desafio_hash, int(time.time()), True))
                    conn2.commit() 
                except mariadb.Error as e: 
                    print(f"Error: {e}")
                print("PARABENS DESAFIO CONLUIDO")
                conn.close()
                conn2.close()
                return True#Como ja inseriu fecha

        #Para os casos em que não existe uma tentativa deste utilizador neste desafio
            #Pode inserir
            #Insere a resolução
            #Grava na BD
        try: 
            cur3 = conn2.cursor()
            cur3.execute(
            "INSERT INTO utilizadores_hash (id_user, id_desafio_hash, data_ultima_tentativa, sucesso) VALUES (?, ?, ?, ?)", 
            (id_user, id_desafio_hash, int(time.time())), True)
            conn2.commit() 
        except mariadb.Error as e: 
            print(f"Error: {e}")
        print("PARABENS DESAFIO CONLUIDO")
        conn.close()
        conn2.close()
        return True

    else:
        conn.close()
        conn2.close()
        print("Desafio errado")
        return False
