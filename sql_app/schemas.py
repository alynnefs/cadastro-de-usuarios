from typing import List, Optional

from pydantic import BaseModel


class AddressBase(BaseModel):

    country: str
    state: str
    city: str
    zip_code: str
    street: str
    number: int
    complement: Optional[str] = None


class AddressCreate(AddressBase):

    pass


class Address(AddressBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):

    id: int
    email: str
    name: str
    cpf: str
    pis: str


class UserCreate(UserBase):

    password: str


class User(UserBase):
    id: int
    is_active: bool
    addresses: List[Address] = []

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(UserLogin):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
