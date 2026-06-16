from pqcrypto.kem.ml_kem_512 import (
    generate_keypair,
    encrypt,
    decrypt
)

print("Generating ML-KEM keypair...")

public_key, secret_key = generate_keypair()

print("Encrypting shared secret...")

ciphertext, shared_secret_1 = encrypt(public_key)

print("Decrypting shared secret...")

shared_secret_2 = decrypt(secret_key, ciphertext)

print()

print("Shared secrets match:")
print(shared_secret_1 == shared_secret_2)