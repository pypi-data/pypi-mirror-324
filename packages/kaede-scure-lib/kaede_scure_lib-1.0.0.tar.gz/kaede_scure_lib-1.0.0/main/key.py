from cryptography.fernet import Fernet # type: ignore

# キー生成
def make_key() -> bytes:
    """新しい暗号鍵を生成"""
    return Fernet.generate_key()

def encrypt_message(message: str, key: bytes) -> bytes:
    """メッセージを暗号化"""
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(token: bytes, key: bytes) -> str:
    """暗号文を復号化"""
    f = Fernet(key)
    return f.decrypt(token).decode()
