from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from .database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    nome = Column(String)
    cpf = Column(String(11))
    pis = Column(String(11))
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    enderecos = relationship("Endereco", back_populates="owner")



class Endereco(Base):

    __tablename__ = "enderecos"


    id = Column(Integer, primary_key=True, index=True)
    pais = Column(String)
    estado = Column(String)
    municipio = Column(String)
    cep = Column(String(8))
    rua = Column(String)
    numero = Column(Integer)
    complemento = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="enderecos")
