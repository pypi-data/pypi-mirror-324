from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import typing
from .security import SecurityManager

Base = declarative_base()

class MasterPassword(Base):
    __tablename__ = 'master_password'
    id = Column(Integer, primary_key=True)
    password_hash = Column(LargeBinary, nullable=False)
    key_salt = Column(LargeBinary, nullable=False)  # For encryption key derivation
    created_at = Column(DateTime, default=datetime.utcnow)

class PasswordEntry(Base):
    __tablename__ = 'password_entries'
    id = Column(Integer, primary_key=True)
    website = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    encrypted_password = Column(LargeBinary, nullable=False)
    entry_salt = Column(LargeBinary, nullable=False)  # Per-entry unique salt
    created_at = Column(DateTime, default=datetime.now)

class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///passwords.db"):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.security = SecurityManager()
        Base.metadata.create_all(self.engine)

    def initialize_master_password(self, password: str) -> bytes:
        """Set up master password for the first time"""
        with self.Session() as session:
            if session.query(MasterPassword).first():
                raise ValueError("Master password already initialized")
            
            if not self.security.check_password_complexity(password):
                raise ValueError("Password does not meet complexity requirements")

            # Generate key derivation salt
            key_salt = self.security.generate_salt()
            
            # Store password hash (Argon2 handles its own salt)
            password_hash = self.security.hash_password(password).encode()
            
            # Create and store master password record
            master_record = MasterPassword(
                password_hash=password_hash,
                key_salt=key_salt
            )
            session.add(master_record)
            session.commit()
            
            # Return derived encryption key
            return self.security.derive_encryption_key(password, key_salt)

    def verify_master_password(self, password: str) -> bytes:
        """Authenticate user and return encryption key"""
        with self.Session() as session:
            master = session.query(MasterPassword).first()
            if not master:
                raise ValueError("Master password not initialized")
            
            # Verify password against stored hash
            if not self.security.verify_password(password, master.password_hash.decode()):
                raise ValueError("Invalid master password")
            
            # Derive encryption key using stored salt
            return self.security.derive_encryption_key(password, master.key_salt)

    def save_password_entry(self, encryption_key: bytes, website: str, email: str, password: str):
        """Store new password entry with unique salt"""
        fernet = self.security.create_fernet(encryption_key)
        entry_salt = self.security.generate_salt()
        
        # Encrypt password with Fernet
        encrypted_password = fernet.encrypt(password.encode())
        
        with self.Session() as session:
            entry = PasswordEntry(
                website=website,
                email=email,
                encrypted_password=encrypted_password,
                entry_salt=entry_salt
            )
            session.add(entry)
            session.commit()

    def get_password_entries(self, encryption_key: bytes, website_filter: str = None) -> typing.List[PasswordEntry]:
        """Retrieve entries with optional filtering"""
        with self.Session() as session:
            query = session.query(PasswordEntry)
            if website_filter:
                query = query.filter(PasswordEntry.website.contains(website_filter))
            return query.all()

    def decrypt_password(self, encryption_key: bytes, encrypted_password: bytes) -> str:
        """Decrypt stored password"""
        fernet = self.security.create_fernet(encryption_key)
        return fernet.decrypt(encrypted_password).decode()