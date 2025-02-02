import os
from cryptography.fernet import Fernet
from passlib.context import CryptContext
import base64
import hashlib
import re

class SecurityManager:
    def __init__(self):
        # Configure Argon2 with security parameters
        self.pwd_context = CryptContext(
            schemes=["argon2"],
            argon2__rounds=4,
            argon2__memory_cost=1024 * 1024,  # 1MB
            argon2__parallelism=4
        )
        
    def generate_salt(self, size: int = 32) -> bytes:
        """Generate cryptographically secure random salt"""
        return os.urandom(size)

    def derive_encryption_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key using PBKDF2-HMAC-SHA256"""
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt,
            iterations=600000,
            dklen=32
        )

    def hash_password(self, password: str) -> str:
        """Hash password using Argon2 (auto-generated salt)"""
        return self.pwd_context.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against stored hash"""
        return self.pwd_context.verify(password, hashed_password)

    def create_fernet(self, key: bytes) -> Fernet:
        """Create Fernet instance from derived key"""
        return Fernet(base64.urlsafe_b64encode(key))

    def check_password_complexity(self, password: str) -> bool:
        """Enforce strong password policy"""
        if len(password) < 12:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>?]", password):
            return False
        return True