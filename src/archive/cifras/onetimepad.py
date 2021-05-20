# https://pypi.org/project/onetimepad/

#-----------------------------------

#IMPORTS

import onetimepad

#-----------------------------------

#INPUT
print("Mensagem a cifrar")
val = input()
print("Chave de cifra")
password = input()

while(val.__len__ != password.__len__):
    print("Chave de Cifra tem que ter o mesmo tamanho que a mensagem a cifrar!")
    print("Chave de cifra")
    password = input()
    
#Encriptar
cipher = onetimepad.encrypt(val, password)

print ("One Time Pad: "+cipher)