#Assistente para criar o config.ini com as credenciais da BD

import configparser
config = configparser.ConfigParser()
print("Assistente de configuração da BD")
print("Utilizador na base de dados")
user = input()
print("Senha base de dados")
password = input()
print("Endereço Servidor")
host = input()
print("Porto")
port = input()
print("Nome Base de Dados")
database = input()
config['DATABASE'] = {'user': user,
                      'password': password,
                      'host':host,
                      'port': port,
                      'database': database}
with open('config.ini', 'w') as configfile:
   config.write(configfile)