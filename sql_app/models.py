from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel

from .database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    cpf = Column(String(11))
    pis = Column(String(11))
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    addresses = relationship("Address", back_populates="owner")



class Address(Base):

    __tablename__ = "addresses"


    id = Column(Integer, primary_key=True, index=True)
    country = Column(String)
    state = Column(String)
    city = Column(String)
    zip_code = Column(String(8))
    street = Column(String)
    number = Column(Integer)
    complement = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="addresses")
