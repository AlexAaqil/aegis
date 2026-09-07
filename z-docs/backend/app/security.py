from cryptography.fernet import Fernet
from app.config import settings

def ensure_key() -> bytes:
    key_path = settings.FERNET_KEY_PATH
    if not key_path.exists():
        key = Fernet.generate_key()
        key_path.write_bytes(key)
        print(f"[INFO] New encryption key created at {key_path}")
    else:
        key = key_path.read_bytes()
        print(f"[INFO] Using existing encryption key from {key_path}")
    return key

FERNET_KEY = ensure_key()
fernet = Fernet(FERNET_KEY)
