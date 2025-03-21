import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:password@localhost/disasterpredict')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-fallback-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    GUARDIAN_KEY = os.getenv('GUARDIAN_KEY')