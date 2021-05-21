from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Hash import SHA256, SHA512, MD5
import binascii

class Cypher:
    def int_of_string(s):
        return int(binascii.hexlify(s), 16)
    
    class ECB:
        TYPE = "ECB"
        
        def encrypt(plaintext, key, mode):
            return AES.new(key, mode).encrypt(plaintext)
        
        def decrypt(ciphertext, key, mode):
            return AES.new(key, mode).decrypt(ciphertext)

    class CBC:
        TYPE = "CBC"
        
        def encrypt(plaintext, key, mode, iv):
            return AES.new(key, mode, iv).encrypt(plaintext)
        
        def decrypt(ciphertext, key, mode, iv):
            return AES.new(key, mode, iv).decrypt(ciphertext)
    
    class CTR:
        TYPE = "CTR"

        def encrypt(plaintext, key, mode, iv):
            return AES.new(key, mode, counter=Counter.new(128, initial_value=Cypher.int_of_string(iv))).encrypt(plaintext)
        
        def decrypt(ciphertext, key, mode, iv):
            return AES.new(key, mode, counter=Counter.new(128, initial_value=Cypher.int_of_string(iv))).decrypt(ciphertext)


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
