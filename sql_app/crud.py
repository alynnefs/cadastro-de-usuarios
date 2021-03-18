from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    # TODO: hash password
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        name=user.name,
        cpf=user.cpf,
        pis=user.pis,
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
