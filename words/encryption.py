import os
import json

from cryptography.fernet import Fernet

TRANSLATOR_ENCRYPTION_KEY = os.environ.get('TRANSLATOR_ENCRYPTION_KEY', default=None)
if not TRANSLATOR_ENCRYPTION_KEY:
    from .ENCRYPTION_KEY import TRANSLATOR_ENCRYPTION_KEY

TRANSLATOR_ENCRYPTION_KEY = TRANSLATOR_ENCRYPTION_KEY.encode()


def do_encrypt(data):
    json_data = json.dumps(data).encode()
    f = Fernet(TRANSLATOR_ENCRYPTION_KEY)
    token = f.encrypt(json_data)
    return token.decode()


def do_decrypt(token):
    f = Fernet(TRANSLATOR_ENCRYPTION_KEY)
    byte_string = f.decrypt(token)
    data = json.loads(byte_string.decode())
    return data


if __name__ == '__main__':
    # testing
    data1 = {
        "word": 'data_from_clipboard',
        'target_language': 'target_language',
        'source_language': 'source_language',
    }
    encrypted_data = do_encrypt(data1)
    print(f"{encrypted_data = }")

    decrypted_data = do_decrypt(encrypted_data)
    print(f"{decrypted_data = }")
