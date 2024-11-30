import os

from flask import Flask

# For a production app, you should use a secret key set in the environment
# The recommended way to generate a 64char secret key is to run:
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

# When deploying, set in the environment to the PostgreSQL URL
SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///db.sqlite3')

EMPLOYEE_ROLE_ID = 1
SUBSCRIBER_ROLE_ID = 2
USER_ROLE_ID = 3

app = Flask(__name__)
