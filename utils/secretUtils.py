import base64
import rsa


def verifyMessage(message, signature, public_key):
    signature_bytes = base64.b64decode(signature)
    pub_key = rsa.PublicKey._load_pkcs1_pem(public_key.encode())
    try:
        result = rsa.verify(
            message.encode('utf-8'), signature_bytes, pub_key)

        is_verified = True

        if result is None:
            is_verified = False

    except rsa.VerificationError:
        is_verified = False

    return is_verified
