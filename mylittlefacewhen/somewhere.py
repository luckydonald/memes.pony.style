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

SUPPORT_EMAIL_ADDRESS = os.getenv('SUPPORT_EMAIL_ADDRESS', 'no-reply@example.com')
SERVER_EMAIL_ADDRESS = os.getenv('SERVER_EMAIL_ADDRESS', 'server@example.com')
DOMAIN = os.getenv('DOMAIN', 'example.com')

EMAIL_SENDER_HOST = os.getenv('EMAIL_SENDER_HOST', 'no-reply@example.com')
EMAIL_SENDER_USER = os.getenv('EMAIL_SENDER_USER', 'server@example.com')
EMAIL_SENDER_PASS = os.getenv('EMAIL_SENDER_PASS', 'server@example.com')

