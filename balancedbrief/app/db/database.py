# balancedbrief/app/db/database.py
import os
import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_db_credentials():
    """Get database credentials from AWS Secrets Manager or environment variables."""
    
    # Check if we're in a testing/development environment
    if os.environ.get('ENV') == 'LOCAL':
        # Use environment variables for local development
        db_pass = os.environ.get('POSTGRES_DB_PASS')
        db_host = os.environ.get('POSTGRES_DB_HOST')
    else:
        # Use AWS Secrets Manager for production
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name="us-west-1")
        secret_name = "bb/config"
        response = client.get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(response["SecretString"])
        db_pass = secret_dict["POSTGRES_DB_PASS"]
        db_host = secret_dict["POSTGRES_DB_HOST"]
    
    return {
        "host": db_host,
        "port": "5432",
        "database": "postgres",
        "user": "postgres",
        "password": db_pass,
    }

def get_db_url():
    """Create database URL from credentials."""
    creds = get_db_credentials()
    # Use pg8000 (pure Python driver)
    return f"postgresql+pg8000://{creds['user']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"

def get_engine():
    """Create SQLAlchemy engine."""
    return create_engine(get_db_url())

def get_session():
    """Create a new database session."""
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

# Base class to be used by all models
Base = declarative_base()