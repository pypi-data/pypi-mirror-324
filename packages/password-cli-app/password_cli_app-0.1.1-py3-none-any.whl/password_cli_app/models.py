# models.py
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PasswordEntry(Base):
    __tablename__ = 'password_entries'
    
    id = Column(Integer, primary_key=True)
    website = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    encrypted_password = Column(LargeBinary, nullable=False)
    password_salt = Column(LargeBinary, nullable=False)  # Per-entry salt
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class MasterPassword(Base):
    __tablename__ = 'master_password'
    id = Column(Integer, primary_key=True)
    password_hash = Column(LargeBinary, nullable=False)
    key_derivation_salt = Column(LargeBinary, nullable=False)  # Master key salt