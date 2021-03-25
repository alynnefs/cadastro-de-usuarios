# run openssl rand -hex 32
SECRET_KEY = "1234567890abcdef1234567890abcdef"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
# in real life, don't put the database name in the example
SQLALCHEMY_DATABASE_URL = "postgresql:///web_user"
SQLALCHEMY_TEST_DATABASE_URL = "postgresql:///test_web_user"
