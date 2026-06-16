import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def generate_hybrid_key():

    # Classical ECDH
    private1 = ec.generate_private_key(ec.SECP384R1())
    private2 = ec.generate_private_key(ec.SECP384R1())

    shared_key = private1.exchange(ec.ECDH(), private2.public_key())

    # Simulated PQ key
    pq_key = os.urandom(32)

    combined = shared_key + pq_key

    session_key = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'cryptexq',
    ).derive(combined)

    return session_key