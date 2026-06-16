from cryptography.hazmat.primitives.asymmetric import ec

from cryptography.hazmat.primitives import hashes

from cryptography.exceptions import InvalidSignature


class SecureSigner:

    def __init__(self):

        self.private_key = (
            ec.generate_private_key(
                ec.SECP256R1()
            )
        )

        self.public_key = (
            self.private_key.public_key()
        )

    def sign(self, data):

        signature = self.private_key.sign(

            data,

            ec.ECDSA(
                hashes.SHA256()
            )
        )

        return signature

    def verify(self, signature, data):

        try:

            self.public_key.verify(

                signature,

                data,

                ec.ECDSA(
                    hashes.SHA256()
                )
            )

            return True

        except InvalidSignature:

            return False