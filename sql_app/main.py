from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/addresses/", response_model=schemas.Address)
def create_address_for_user(
    user_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)
):
    return crud.create_user_address(db=db, address=address, user_id=user_id)

@app.get("/users/{user_id}/addresses/")
def read_address_by_id(
    user_id: int, db: Session = Depends(get_db)
):
    return crud.get_address_by_id(db=db, id=user_id)

@app.get("/addresses/", response_model=List[schemas.Address])
def read_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_addresses(db, skip=skip, limit=limit)

@app.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    return crud.delete_user(db=db, user_id=user_id)

@app.put("/users/{user_id}/addresses/{address_id}", response_model=schemas.Address)
def update_address(
    user_id: int, address_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)
):
    return crud.update_address(db=db, address=address, owner_id=user_id, address_id=address_id)
