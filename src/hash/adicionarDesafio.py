import mariadb
from Crypto.Hash import SHA256, SHA512, MD5
#leitura do config.ini
import configparser
config = configparser.ConfigParser()
config.read('src/login/config.ini')

#fim leitura do config.ini

id_user = 27

print ("Adicionar Desafio de Hash")
print ("Indique o algoritmo (MD5, SHA256, SHA512)")
#Necessao validar input#
algoritmo = input()
print ("Indique a dica")
dica = input()
print ("Indique a mensagem")
msg = input().encode()
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
if (algoritmo == "MD5"):
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
    print("Registo efectuado com sucesso - Let the challenges beggin!")
    conn.close()

if (algoritmo == "SHA256"):
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
    print("Registo efectuado com sucesso - Let the challenges beggin!")
    conn.close()

if (algoritmo == "SHA512"):
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
    print("Desadio inserido com sucesso!")
    conn.close()