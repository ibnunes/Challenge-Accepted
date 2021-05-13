# https://pycryptodome.readthedocs.io/en/latest/src/hash/hash.html

#-----------------------------------

#IMPORTS

import hashlib
from Crypto.Hash import SHA256, SHA512, MD5

#-----------------------------------

#INPUT
print("Mensagem a cifrar")
val = input().encode()

plaintext=val

#-----------------------------------
#TYPES OF HASHES

#SHA256

#USING HASHLIB
m = hashlib.sha256()
m.update(val)
word_hash = m.hexdigest()

#USING CRYPTO
#h = SHA256.new()
#h.update(val)
#print(h.hexdigest())

print ("Hash (SHA256): "+word_hash)

#-----------------------------------

#SHA512

#USING HASHLIB
m = hashlib.sha512()
m.update(val)
word_hash = m.hexdigest()

#USING CRYPTO
#h = SHA512.new()
#h.update(val)
#print(h.hexdigest())

print ("Hash (SHA512): "+word_hash)

#-----------------------------------

#MD5

#USING HASHLIB
m = hashlib.md5()
m.update(val)
word_hash = m.hexdigest()

#USING CRYPTO
#h = MD5.new()
#h.update(val)
#print(h.hexdigest())

print ("Hash (MD5): "+word_hash)

#-----------------------------------