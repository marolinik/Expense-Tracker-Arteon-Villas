import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # PostgreSQL Database Configuration
    # Format: postgresql://username:password@localhost:port/database_name
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:password@localhost:5432/arteon_villas_expenses'
    
    # Alternative connection string formats:
    # 'postgresql://postgres:password@localhost/arteon_villas_expenses'
    # 'postgresql+psycopg2://postgres:password@localhost:5432/arteon_villas_expenses'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24) 