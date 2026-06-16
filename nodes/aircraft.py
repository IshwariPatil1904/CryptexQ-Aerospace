from simulation.telemetry import generate_telemetry

from core.encryption import encrypt_message

from core.signatures import SecureSigner


def aircraft_send(key):

    telemetry = generate_telemetry()

    nonce, encrypted = encrypt_message(
        key,
        telemetry
    )

    # Create signer
    signer = SecureSigner()

    # Sign encrypted packet
    signature = signer.sign(encrypted)

    return (

        telemetry,

        nonce,

        encrypted,

        signature,

        signer.public_key
    )