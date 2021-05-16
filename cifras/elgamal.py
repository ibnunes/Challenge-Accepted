# https://pypi.org/project/elgamal/#files
from elgamal.elgamal import Elgamal

#INPUT
print("Mensagem a cifrar")
val = input()
print("Chave de cifra")
password = input()

cipher = Elgamal.encrypt(val, password)