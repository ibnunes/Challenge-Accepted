#https://pypi.org/project/vigenere/
from vigenere import encrypt

#INPUT
print("Mensagem a cifrar")
val = input()
print("Chave de cifra")
password = input()

cipher = encrypt(val, password)
