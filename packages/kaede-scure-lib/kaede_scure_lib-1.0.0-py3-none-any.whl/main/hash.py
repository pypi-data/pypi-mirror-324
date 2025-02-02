import hashlib

def hash_password(password: str) -> str:
    """パスワードをSHA-256でハッシュ化"""
    return hashlib.sha256(password.encode()).hexdigest()
