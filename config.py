import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL_UNPOOLED')
    SQLALCHEMY_TRACK_MODIFICATIONS = False