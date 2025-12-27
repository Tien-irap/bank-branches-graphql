"""
SQL Models - The "Database"
Note: Currently using raw SQLite with sqlite3.
This file is prepared for future SQLAlchemy migration.

For now, the database schema is:
- banks(id, name)
- branches(ifsc, branch, address, city, district, state, bank_id)
"""
from app.core.logger import logger

# TODO: Migrate to SQLAlchemy models when needed
# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class Bank(Base):
#     __tablename__ = 'banks'
#     id = Column(Integer, primary_key=True)
#     name = Column(String, unique=True, nullable=False)
#     branches = relationship("Branch", back_populates="bank")
#
# class Branch(Base):
#     __tablename__ = 'branches'
#     ifsc = Column(String, primary_key=True)
#     branch = Column(String)
#     address = Column(String)
#     city = Column(String)
#     district = Column(String)
#     state = Column(String)
#     bank_id = Column(Integer, ForeignKey('banks.id'))
#     bank = relationship("Bank", back_populates="branches")

logger.info("SQL models module loaded (currently using raw SQLite)")
