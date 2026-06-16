import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_message(key, message):

    aes = AESGCM(key)
    nonce = os.urandom(12)

    ciphertext = aes.encrypt(nonce, message.encode(), None)

    return nonce, ciphertext


def decrypt_message(key, nonce, ciphertext):

    aes = AESGCM(key)

    plaintext = aes.decrypt(nonce, ciphertext, None)

    return plaintext.decode()