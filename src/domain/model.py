from datetime import datetime
from sqlalchemy import (
    Boolean, Column, 
    DateTime, ForeignKey, 
    Integer, String, Text)
from sqlalchemy.orm import relationship
from src.adpater.sqlite_connexion import Base


class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    username = Column(String(170), unique=True)
    email = Column(String(120), unique=True)
    password = Column(Text)
    auth_id = relationship("Authenticates")
    
    
class Tokens(Base):
    __tablename__ = "Tokens"
    id = Column(Integer, primary_key=True)
    access_key = Column(Text, nullable=False)
    create_at = Column(DateTime, default=datetime.now() , nullable=False)
    espirated_at = Column(DateTime, default=datetime.now() , nullable=False)
    auth_id = Column(Integer, ForeignKey("Authenticates.id"))
    
    
class Authenticates(Base):
    __tablename__ = "Authenticates"
    id = Column(Integer, primary_key=True, unique=True)
    status = Column(Boolean, default=True, nullable=False)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    create_at = Column(DateTime, default=datetime.now() , nullable=False)
    tokens = relationship("Tokens")
    