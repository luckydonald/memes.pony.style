import os


DJANGO_SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', None)
assert DJANGO_SECRET_KEY is not None  # $DJANGO_SECRET_KEY environment variable
SECRET_KEY = DJANGO_SECRET_KEY


POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME', None)
assert POSTGRES_DB_NAME is not None  # $POSTGRES_DB_NAME environment variable

POSTGRES_DB_USER = os.getenv('POSTGRES_DB_USER', None)
assert POSTGRES_DB_USER is not None  # $POSTGRES_DB_USER environment variable

POSTGRES_DB_PASS = os.getenv('POSTGRES_DB_PASS', None)
assert POSTGRES_DB_PASS is not None  # $POSTGRES_DB_PASS environment variable

POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST', None)
assert POSTGRES_DB_HOST is not None  # $POSTGRES_DB_HOST environment variable

POSTGRES_DB_PORT = os.getenv('POSTGRES_DB_PORT', None)


DB_CONF = {
    "dbname": POSTGRES_DB_NAME,
    "username": POSTGRES_DB_USER,
    "password": POSTGRES_DB_PASS,
    "host": POSTGRES_DB_HOST,
    "port": POSTGRES_DB_PORT,
}


EMAIL_CONF = {
    "username": "email uiser",
    "password": "asdasdasd",
}
