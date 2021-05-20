# https://pypi.org/project/elgamal/
from elgamal.elgamal import Elgamal

#INPUT
print("Mensagem a cifrar")
val = input()

passpub, passpriv = Elgamal.newkeys(128)

cipher = Elgamal.encrypt(val, passpub)

print ("Elgamal: "+cipher)