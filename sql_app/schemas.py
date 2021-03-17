from typing import List, Optional

from pydantic import BaseModel


class EnderecoBase(BaseModel):

    pais: str
    estado: str
    municipio: str
    cep: str
    rua: str
    numero: int
    complemento: Optional[str] = None


class EnderecoCreate(EnderecoBase):

    pass


class Endereco(EnderecoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):

    email: str
    id: int
    email: str
    nome: str
    cpf: str
    pis: str


class UserCreate(UserBase):

    password: str


class User(UserBase):
    id: int
    is_active: bool
    enderecos: List[Endereco] = []

    class Config:
        orm_mode = True
