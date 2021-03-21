from datetime import datetime, timedelta
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine
from .utils import get_db
from .local_settings import ACCESS_TOKEN_EXPIRE_MINUTES


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_cpf = crud.get_user_by_cpf(db, cpf=user.cpf)
    db_user_pis = crud.get_user_by_pis(db, pis=user.pis)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_cpf:
        raise HTTPException(status_code=400, detail="CPF already registered")
    if db_user_pis:
        raise HTTPException(status_code=400, detail="PIS already registered")
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

@app.delete("/addresses/{address_id}/")
def delete_address_by_id(address_id: int, db: Session = Depends(get_db)):
    return crud.delete_address_by_id(db=db, address_id=address_id)

@app.delete("/users/{user_id}/addresses/")
def delete_all_addresses_by_id(user_id: int, db: Session = Depends(get_db)):
    return crud.delete_all_addresses(db=db, user_id=user_id)

@app.put("/users/{user_id}/addresses/{address_id}/", response_model=schemas.Address)
def update_address(
    user_id: int, address_id: int, address: schemas.AddressCreate, db: Session = Depends(get_db)
):
    return crud.update_address(db=db, address=address, owner_id=user_id, address_id=address_id)

# Security
@app.get("/items/")
async def read_items(token: str = Depends(crud.oauth2_scheme)):
    return {"token": token}

@app.get("/users/me")
def read_users_me(current_user: schemas.UserLogin = Depends(crud.get_current_user)):
    return current_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect e-mail or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
