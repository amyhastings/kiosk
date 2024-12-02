import os

from flask import Flask

SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

SQLALCHEMY_DATABASE_URI = os.getenv('LOCAL_DATABASE_URL', 'sqlite:///db.sqlite3')

# Global variables
EMPLOYEE_ROLE_ID = 1
SUBSCRIBER_ROLE_ID = 2
USER_ROLE_ID = 3

app = Flask(__name__)
