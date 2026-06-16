from core.encryption import decrypt_message

from core.signatures import SecureSigner


def ground_receive(

    key,

    nonce,

    encrypted,

    signature,

    public_key
):

    verifier = SecureSigner()

    verifier.public_key = public_key

    valid = verifier.verify(
        signature,
        encrypted
    )

    if not valid:

        raise Exception(
            "Digital signature verification failed"
        )

    message = decrypt_message(
        key,
        nonce,
        encrypted
    )

    return message