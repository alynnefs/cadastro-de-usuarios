from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from .utils import is_cpf_valid, is_pis_valid, is_email_valid, remove_characters
from .local_settings import ALGORITHM, SECRET_KEY
from . import models, schemas
from .utils import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_cpf(db: Session, cpf: str):

    return db.query(models.User).filter(models.User.cpf == cpf).first()

def get_user_by_pis(db: Session, pis: str):

    return db.query(models.User).filter(models.User.pis == pis).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if (not is_cpf_valid(user.cpf)):
        raise HTTPException(status_code=400, detail="Invalid CPF")

    if (not is_pis_valid(user.pis)):
        raise HTTPException(status_code=400, detail="Invalid PIS")

    if (not is_email_valid(user.email)):
        raise HTTPException(status_code=400, detail="Invalid e-mail")

    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        name=user.name,
        cpf=remove_characters(user.cpf),
        pis=remove_characters(user.pis),
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_addresses(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Address).offset(skip).limit(limit).all()


def get_address_by_id(db: Session, id: int):

    return db.query(models.Address).filter(models.Address.owner_id == id).all()


def create_user_address(db: Session, address: schemas.AddressCreate, user_id: int):
    db_address = models.Address(**address.dict(), owner_id=user_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def delete_all_addresses(db: Session, user_id:int):
    addresses = db.query(models.Address).filter(models.Address.owner_id == user_id).all()
    for address in addresses:
        db.delete(address)
        db.commit()
    return addresses


def delete_address_by_id(db: Session, address_id:int):
    db_address = db.query(models.Address).filter(models.Address.id == address_id).first()
    db.delete(db_address)
    db.commit()

    return db_address


def delete_user(db: Session, user_id:int):
    delete_all_addresses(db=db, user_id=user_id)
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()

    return db_user

def update_address(db: Session, address: schemas.AddressCreate, owner_id: int, address_id: int):
    db_address = models.Address(**address.dict(), owner_id=owner_id, id=address_id)
    db.merge(db_address)
    db.commit()

    return db_address


# security
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_json(db: Session, email):
    user = get_user_by_email(db, email)

    return {
        "email": user.email,
        "name": user.name
    }

def authenticate_user(db, username: str, password: str):
    user = get_user_by_email(db, email=username)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # username is the field name, but it is the email
    user = get_user_json(db=db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: schemas.UserLogin = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
