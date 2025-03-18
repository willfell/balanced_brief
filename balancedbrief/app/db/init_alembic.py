#!/usr/bin/env python3
# balancedbrief/app/db/init_alembic.py
import os
import sys
import subprocess
import logging
from alembic.config import Config
from alembic import command

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def initialize_alembic():
    """Initialize the Alembic environment."""
    try:
        # Get the directory containing this script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Path to alembic.ini
        alembic_ini = os.path.join(base_dir, 'alembic.ini')
        
        # Create alembic directory if it doesn't exist
        alembic_dir = os.path.join(base_dir, 'alembic')
        if not os.path.exists(alembic_dir):
            os.makedirs(alembic_dir, exist_ok=True)
            logger.info(f"Created Alembic directory at {alembic_dir}")
        
        # Check if the versions directory exists
        versions_dir = os.path.join(alembic_dir, 'versions')
        if not os.path.exists(versions_dir):
            os.makedirs(versions_dir, exist_ok=True)
            logger.info(f"Created versions directory at {versions_dir}")
        
        # Get the Alembic configuration
        alembic_cfg = Config(alembic_ini)
        
        # Initialize Alembic
        logger.info("Initializing Alembic...")
        command.init(alembic_cfg, alembic_dir)
        logger.info("Alembic initialized successfully")
        
        # Generate initial migration
        logger.info("Generating initial migration...")
        command.revision(alembic_cfg, message="Initial migration", autogenerate=True)
        logger.info("Initial migration generated successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing Alembic: {e}")
        return False

if __name__ == "__main__":
    if initialize_alembic():
        sys.exit(0)
    else:
        sys.exit(1)