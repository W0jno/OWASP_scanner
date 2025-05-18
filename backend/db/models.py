from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base

""" class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String) """

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    #user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String, nullable=False)
    status = Column(String, nullable=True)
    result = Column(String, nullable=True)
    created_at = Column(DateTime)

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    vulnerability_type = Column(String)
    description = Column(String)
    severity = Column(String)
    created_at = Column(DateTime)