import os
import base64

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

def generate_wireguard_keys() -> [str, str, str]:
    private_key = x25519.X25519PrivateKey.generate()

    public_key = private_key.public_key()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    preshared_key = os.urandom(32)
    private_key_base64 = base64.b64encode(private_key_bytes).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key_bytes).decode('utf-8')
    preshared_key_base64 = base64.b64encode(preshared_key).decode('utf-8')


    return private_key_base64, public_key_base64, preshared_key_base64
