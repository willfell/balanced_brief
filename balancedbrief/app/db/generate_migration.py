import os
import sys
import subprocess
from alembic import command
from alembic.config import Config

def main():
    """Generate the initial migration from SQLAlchemy models."""
    # Get the absolute path to the alembic.ini file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini = os.path.join(base_dir, 'alembic.ini')
    
    # Create an Alembic configuration object
    alembic_cfg = Config(alembic_ini)
    
    # Initialize Alembic if it hasn't been initialized
    versions_dir = os.path.join(base_dir, 'alembic', 'versions')
    if not os.path.exists(versions_dir):
        print("Initializing Alembic...")
        os.makedirs(versions_dir, exist_ok=True)
    
    # Generate a migration script
    message = "Initial migration"
    print(f"Generating initial migration: {message}")
    command.revision(alembic_cfg, message=message, autogenerate=True)
    
    print("Migration script generated successfully.")

if __name__ == "__main__":
    main()