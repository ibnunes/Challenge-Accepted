# https://pypi.org/project/caesarcipher/
from caesarcipher import CaesarCipher

#INPUT
print("Mensagem a cifrar")
val = input()


cipher = CaesarCipher(val).encoded


print ("Ceaser: "+cipher)
