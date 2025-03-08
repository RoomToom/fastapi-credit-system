from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    registration_date = Column(Date)

class Credit(Base):
    __tablename__ = "credits"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    issuance_date = Column(Date)
    return_date = Column(Date)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Float)
    percent = Column(Float)
    user = relationship("User")

class Dictionary(Base):
    __tablename__ = "dictionary"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    period = Column(Date)
    sum = Column(Float)
    category_id = Column(Integer, ForeignKey("dictionary.id"))
    category = relationship("Dictionary")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    sum = Column(Float)
    payment_date = Column(Date)
    credit_id = Column(Integer, ForeignKey("credits.id"))
    type_id = Column(Integer, ForeignKey("dictionary.id"))
    credit = relationship("Credit")
    type = relationship("Dictionary")
