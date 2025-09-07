import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1) if os.getenv('DATABASE_URL') else 'sqlite:///../instance/disaster.db'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-fallback-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    GUARDIAN_KEY = os.getenv('GUARDIAN_KEY')
