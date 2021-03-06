from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..backend.database import Base
from ..backend.main import app
from ..backend.utils import get_db
from ..backend.local_settings import SQLALCHEMY_TEST_DATABASE_URL


engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL
)

TestingSessionLocal = sessionmaker(
                      autocommit=False,
                      autoflush=False,
                      bind=engine
                      )

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/users/",
        json={
            "id": 1,
            "email": "deadpool@example.com",
            "password": "chimichangas4life",
            "name": "Deadpool",
            "cpf": "43987702834",
            "pis": "12090310016"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert "id" in data
    user_id = data["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "deadpool@example.com"
    assert data["name"] == "Deadpool"
    assert data["cpf"] == "43987702834"
    assert data["pis"] == "12090310016"


def get_user_by_id():
    user_id = 1
    response = client.get(
        f"/users/{user_id}/"
    )
    assert response.status_code == 200


def create_address():
    user_id = 1
    response = client.post(
        f"/users/{user_id}/adresses/",
        json={
            "id": 1,
            "country": "Brasil",
            "state": "Ceará",
            "city": "Pacatuba",
            "zip_code": "61800000",
            "street": "rua dos bobos",
            "number": 123,
            "complement": "A"
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["zip_code"] == "61800000"
    assert "id" in data
    address_id = data["id"]

    response = client.get(f"/users/{user_id}/addresses/{address_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == address_id
    assert data["country"] == "Brasil"
    assert data["state"] == "Ceará"
    assert data["city"] == "Pacatuba"
    assert data["zip_code"] == "61800000"
    assert data["street"] == "rua dos bobos"
    assert data["number"] == 123
    assert data["complement"] == "A"


def get_address_by_user_id():
    user_id = 1
    response = client.get(
        f"/users/{user_id}/addresses/"
    )
    assert response.status_code == 200


def update_address():
    user_id = 1
    response = client.post(
        f"/users/{user_id}/adresses/",
        json={
            "id": 1,
            "country": "Argentina",
            "state": "Mendoza",
            "city": "La Paz",
            "zip_code": "00005590",
            "street": "calle de las manzanas",
            "number": 456,
            "complement": "b"
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["zip_code"] == "00005590"
    assert "id" in data
    address_id = data["id"]

    response = client.get(f"/users/{user_id}/addresses/{address_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == address_id
    assert data["country"] == "Argentina"
    assert data["state"] == "Mendoza"
    assert data["city"] == "La Paz"
    assert data["zip_code"] == "00005590"
    assert data["street"] == "calle de las manzanas"
    assert data["number"] == 456
    assert data["complement"] == "B"


def test_delete_user():
    user_id = 1
    response = client.delete(
        f"/users/{user_id}/"
    )
    assert response.status_code == 200, response.text


def test_get_addresses():
    response = client.get("/addresses/")
    assert response.status_code == 200
