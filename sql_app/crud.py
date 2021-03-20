from sqlalchemy.orm import Session
from fastapi import HTTPException

from .utils import is_cpf_valid, is_pis_valid, is_email_valid, remove_characters
from . import models, schemas


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
    # TODO: hash password
    if (not is_cpf_valid(user.cpf)):
        raise HTTPException(status_code=400, detail="Invalid CPF")

    if (not is_pis_valid(user.pis)):
        raise HTTPException(status_code=400, detail="Invalid PIS")

    if (not is_email_valid(user.email)):
        raise HTTPException(status_code=400, detail="Invalid e-mail")

    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        name=user.name,
        cpf=remove_characters(user.cpf),
        pis=remove_characters(user.pis),
        hashed_password=fake_hashed_password
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
