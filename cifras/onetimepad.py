# https://pypi.org/project/onetimepad/

#-----------------------------------

#IMPORTS

from  PyPi import onetimepad

#-----------------------------------

#INPUT
print("Mensagem a cifrar")
val = input()
print("Chave de cifra")
password = input()

while(len(val) != len(password)):
    print("Chave de Cifra tem que ter o mesmo tamanho que a mensagem a cifrar!")
    print("Chave de cifra")
    password = input()
    
#Encriptar
cipher = onetimepad.encrypt(val, password)

print ("One Time Pad: "+cipher)
