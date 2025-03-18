# db/migrate.py
import os
import sys
import logging
import argparse
import boto3
import json
from alembic import command
from alembic.config import Config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_db_credentials():
    """Get database credentials from AWS Secrets Manager or environment variables."""
    client = boto3.client('secretsmanager')
    secret_name = "bb/config"

    try:
        response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in response:
            secret = response['SecretString']
        else:
            secret = response['SecretBinary']
        secret_dict = json.loads(secret)

        if os.environ['ENV'] == "PROD":
            DB_PASS = secret_dict['POSTGRES_DB_PASS']
            DB_HOST = secret_dict['POSTGRES_DB_HOST']
        else:
            DB_PASS = os.environ['POSTGRES_DB_PASS']
            DB_HOST = os.environ['POSTGRES_DB_HOST']
        
        return {
            'user': 'postgres',
            'password': DB_PASS,
            'host': DB_HOST,
            'port': '5432',
            'database': 'postgres'
        }
    except Exception as e:
        logger.error(f"Error getting database credentials: {e}")
        raise

def run_migrations():
    """Run all pending Alembic migrations."""
    try:
        # Add parent directory to Python path to find the Alembic config
        parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'balancedbrief', 'app')
        sys.path.insert(0, parent_dir)
        
        # Get the Alembic config file path
        alembic_dir = os.path.join(parent_dir, 'db')
        alembic_ini = os.path.join(alembic_dir, 'alembic.ini')
        
        if not os.path.exists(alembic_ini):
            logger.error(f"Alembic config file not found at {alembic_ini}")
            return False
        
        # Create an Alembic configuration object
        alembic_cfg = Config(alembic_ini)
        
        # Run the migrations
        logger.info("Running database migrations...")
        command.upgrade(alembic_cfg, "head")
        
        logger.info("Migrations completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error running migrations: {e}")
        return False

def seed_data():
    """Seed initial data into the database if needed."""
    # This function could be used to insert initial data after migrations
    # such as parent categories, subreddits, etc.
    pass

def main():
    parser = argparse.ArgumentParser(description='Run database migrations using Alembic')
    parser.add_argument('--seed', action='store_true', help='Seed initial data after migrations')
    args = parser.parse_args()
    
    if run_migrations():
        if args.seed:
            seed_data()
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())