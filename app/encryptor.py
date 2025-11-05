# app/encryptor.py
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

USER_KEY_FILE = os.path.join(os.path.expanduser("~"), ".animexstream_key")

def ensure_key():
    # Create key if not exists. For production, wrap with Android Keystore using keystore.py
    if not os.path.exists(USER_KEY_FILE):
        key = get_random_bytes(32)  # AES-256
        with open(USER_KEY_FILE, "wb") as f:
            f.write(key)
        try:
            os.chmod(USER_KEY_FILE, 0o600)
        except Exception:
            pass
    return True

def load_key():
    with open(USER_KEY_FILE, "rb") as f:
        return f.read()

def encrypt_file_stream(in_path, out_path, key=None, chunk_size=1024*1024):
    if key is None:
        key = load_key()
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    with open(in_path, "rb") as inf, open(out_path, "wb") as outf:
        outf.write(nonce)  # 12 bytes
        while True:
            chunk = inf.read(chunk_size)
            if not chunk:
                break
            outf.write(cipher.encrypt(chunk))
        tag = cipher.digest()
        outf.write(tag)  # 16 bytes
    return out_path

def secure_delete(path):
    # best-effort overwrite then delete
    try:
        if os.path.exists(path):
            length = os.path.getsize(path)
            with open(path, "r+b") as f:
                f.seek(0)
                f.write(b'\x00' * max(1024, min(length, 1024*1024)))
            os.remove(path)
    except Exception:
        try:
            os.remove(path)
        except Exception:
            pass