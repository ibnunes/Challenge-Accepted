import mariadb
from prettytable import PrettyTable
from prettytable import from_db_cursor

#leitura do config.ini
import configparser
config = configparser.ConfigParser()
config.read('src/login/config.ini')
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

x = PrettyTable()

cur = conn.cursor()
cur.execute(
    "SELECT desafios_hash.id_desafio_hash as ID, desafios_hash.algoritmo , utilizadores.username as 'Proposto por' FROM desafios_hash INNER JOIN utilizadores ON desafios_hash.id_user=utilizadores.id_user")
x = from_db_cursor(cur) 



print(x)

#print(tabulate(table, headers='firstrow', showindex='always'))




