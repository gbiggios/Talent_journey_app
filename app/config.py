from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables desde el archivo .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    CSRF_ENABLED = os.getenv('CSRF_ENABLED', 'True').lower() in ['true', '1', 't']
    WTF_CSRF_ENABLED = os.getenv('WTF_CSRF_ENABLED', 'True').lower() in ['true', '1', 't']
