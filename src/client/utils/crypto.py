from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import SHA256, SHA512, MD5
import binascii
from sympy.crypto.crypto import encipher_vigenere
from sympy.crypto.crypto import decipher_vigenere
import pycaesarcipher
import onetimepad

class Cypher:
    def int_of_string(s):
        return int(binascii.hexlify(s), 16)
    
    class ECB:
        TYPE = "ECB"
        
        def encrypt(plaintext, key, mode):
            return AES.new(key, mode).encrypt(plaintext).decode()
        
        def decrypt(ciphertext, key, mode):
            return AES.new(key, mode).decrypt(ciphertext).decode()

    class CBC:
        TYPE = "CBC"
        
        def encrypt(plaintext, key, mode, iv):
            return AES.new(key, mode, iv).encrypt(plaintext).decode()
        
        def decrypt(ciphertext, key, mode, iv):
            return AES.new(key, mode, iv).decrypt(ciphertext).decode()
    
    class CTR:
        TYPE = "CTR"

        def encrypt(plaintext, key, mode, iv):
            return AES.new(key, mode, counter=Counter.new(128, initial_value=Cypher.int_of_string(iv))).encrypt(plaintext).decode()
        
        def decrypt(ciphertext, key, mode, iv):
            return AES.new(key, mode, counter=Counter.new(128, initial_value=Cypher.int_of_string(iv))).decrypt(ciphertext).decode()

    class OTP:
        TYPE = "ONETIMEPAD"

        def encrypt(plaintext, key):
            return onetimepad.encrypt(plaintext, key)

        def decrypt(ciphertext, key):
            return onetimepad.decrypt(bytearray(ciphertext).decode(), key)

    class Vigenere:
        TYPE = "VIGENERE"

        def encrypt(plaintext, key):
            return encipher_vigenere(plaintext, key)

        def decrypt(ciphertext, key):
            return decipher_vigenere(bytearray(ciphertext).decode(), key)

    class Caesar:
        TYPE = "CAESAR"

        def encrypt(plaintext, key):
            return pycaesarcipher.pycaesarcipher().caesar_encipher(plaintext, key)

        def decrypt(ciphertext, key):
            return pycaesarcipher.pycaesarcipher().caesar_decipher(bytearray(ciphertext).decode(), key)


class Hash:
    class MD5:
        TYPE = "MD5"

        def encrypt(plaintext):
            h = MD5.new()
            h.update(plaintext)
            return h.hexdigest()

    class SHA256:
        TYPE = "SHA256"

        def encrypt(plaintext):
            h = SHA256.new()
            h.update(plaintext)
            return h.hexdigest()

    class SHA512:
        TYPE = "SHA512"

        def encrypt(plaintext):
            h = SHA512.new()
            h.update(plaintext)
            return h.hexdigest()
