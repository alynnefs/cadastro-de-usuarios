from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        nome=user.nome,
        cpf=user.cpf,
        pis=user.pis,
        hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_enderecos(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Endereco).offset(skip).limit(limit).all()


def get_address_by_id(db: Session, id: int):
    
    return db.query(models.Endereco).filter(models.Endereco.owner_id == id).all()


def create_user_endereco(db: Session, endereco: schemas.EnderecoCreate, user_id: int):
    db_endereco = models.Endereco(**endereco.dict(), owner_id=user_id)
    db.add(db_endereco)
    db.commit()
    db.refresh(db_endereco)
    return db_endereco
