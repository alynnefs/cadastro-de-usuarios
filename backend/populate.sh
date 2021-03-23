# user 1
user_id=$(curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "email": "alynne@gmail.com",
  "name": "Alynne",
  "cpf": "411.486.264-17",
  "pis": "12021454551",
  "password": "alynne123"
}' | jq -r '.id')

curl -X 'POST' \
  'http://127.0.0.1:8000/users/'$user_id'/addresses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "country": "Brasil",
  "state": "Ceará",
  "city": "Pacatuba",
  "zip_code": "61800000",
  "street": "rua dos bobos",
  "number": 0,
  "complement": ""
}'

# user 2
user_id=$(curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "email": "maria@gmail.com",
  "name": "Maria",
  "cpf": "468.018.600-38",
  "pis": "12023522147",
  "password": "maria123"
}' | jq -r '.id')


curl -X 'POST' \
  'http://127.0.0.1:8000/users/'$user_id'/addresses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "country": "Brasil",
  "state": "Ceará",
  "city": "Fortaleza",
  "zip_code": "63700000",
  "street": "Av. Treze de Maio",
  "number": 2081,
  "complement": "IFCE"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/users/'$user_id'/addresses/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "country": "Brasil",
  "state": "Ceará",
  "city": "Fortaleza",
  "zip_code": "60160110",
  "street": "Rua Ana Bilhar",
  "number": 1136,
  "complement": "B"
}'
