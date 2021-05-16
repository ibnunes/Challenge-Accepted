# https://asecuritysite.com/encryption/aes_modes
# https://stackoverflow.com/questions/3154998/pycrypto-problem-using-aesctr

from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
import sys
import binascii
import Padding
import base64

print("Mensagem a cifrar")
val = input()
print("Chave de cifra")
password = input()
ival=10

if (len(sys.argv)>1):
	val=sys.argv[1]

if (len(sys.argv)>2):
	password=str(sys.argv[2])

if (len(sys.argv)>3):
	ival=int(sys.argv[3])

plaintext=val

def encrypt(plaintext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.encrypt(plaintext))

def decrypt(ciphertext,key, mode):
	encobj = AES.new(key,mode)
	return(encobj.decrypt(ciphertext))

def encrypt2(plaintext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.encrypt(plaintext))

def decrypt2(ciphertext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.decrypt(ciphertext))

def int_of_string(s):
    return int(binascii.hexlify(s), 16)

def encrypt3(plaintext,key, mode, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    encobj = AES.new(key,mode,counter=ctr)
    return(encobj.encrypt(plaintext))

def decrypt3(ciphertext,key, mode, iv):
    ctr = Counter.new(128, initial_value=int_of_string(iv))
    encobj = AES.new(key,mode,counter=ctr)
    return(encobj.decrypt(ciphertext))

#Gerar um hash de 128bits pra uso como key no AES
#Derivação da password
key = hashlib.md5(password.encode()).digest()

iv= hex(ival)[2:8].zfill(16)
print ("IV: "+iv)	

#ECB
plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)
print ("Input data (CMS): "+binascii.hexlify(plaintext.encode()).decode())

ciphertext = encrypt(plaintext.encode(),key,AES.MODE_ECB)
#String a guardar na BD
msg = base64.b64encode(bytearray(ciphertext)).decode()
print ("Cipher (ECB): "+ msg)


plaintext = decrypt(base64.b64decode(msg),key,AES.MODE_ECB)
plaintext = Padding.removePadding(plaintext.decode(),mode=0)
print ("  decrypt: "+plaintext)


#CBC

plaintext=val
plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

ciphertext = encrypt2(plaintext.encode(),key,AES.MODE_CBC,iv.encode())
print ("Cipher (CBC): "+binascii.hexlify(bytearray(ciphertext)).decode())

plaintext = decrypt2(ciphertext,key,AES.MODE_CBC,iv.encode())
plaintext = Padding.removePadding(plaintext.decode(),mode=0)
print ("  decrypt: "+plaintext)


#CTR

plaintext=val
plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

ciphertext = encrypt3(plaintext.encode(),key,AES.MODE_CTR,iv.encode())
print ("Cipher (CTR): "+binascii.hexlify(bytearray(ciphertext)).decode())

plaintext = decrypt3(ciphertext,key,AES.MODE_CTR,iv.encode())
plaintext = Padding.removePadding(plaintext.decode(),mode=0)
print ("  decrypt: "+plaintext)
