# Balanced Brief Local Development Setup

This guide explains how to set up and use a local PostgreSQL database in Docker for development and testing, along with Alembic for database migrations.

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ with pip
- `psycopg2-binary`, `alembic`, and `sqlalchemy` Python packages

## Quick Start

1. Make the helper script executable:
   ```bash
   chmod +x db-helper.sh
   ```

2. Start the PostgreSQL database and set up the development environment:
   ```bash
   ./db-helper.sh setup
   ```

3. Initialize Alembic (if not already initialized):
   ```bash
   ./db-helper.sh db:init
   ```

4. Create your first migration:
   ```bash
   ./db-helper.sh db:auto "Initial migration"
   ```

5. Apply migrations:
   ```bash
   ./db-helper.sh db:upgrade head
   ```

## Using the Database Helper Script

The `db-helper.sh` script provides a unified interface for managing both your PostgreSQL database and Alembic migrations.

### PostgreSQL Commands

- **Start PostgreSQL**: `./db-helper.sh pg:start`
- **Stop PostgreSQL**: `./db-helper.sh pg:stop`
- **Check status**: `./db-helper.sh pg:status`
- **View logs**: `./db-helper.sh pg:logs`
- **Connect with psql**: `./db-helper.sh pg:connect`
- **Reset database** (removes all data): `./db-helper.sh pg:reset`

### Alembic Commands

- **Initialize Alembic**: `./db-helper.sh db:init`
- **Create empty migration**: `./db-helper.sh db:revision "Add user table"`
- **Auto-generate migration**: `./db-helper.sh db:auto "Add user table"`
- **Upgrade database**: `./db-helper.sh db:upgrade head`
- **Downgrade database**: `./db-helper.sh db:downgrade -1`
- **Show current revision**: `./db-helper.sh db:current`
- **Show revision history**: `./db-helper.sh db:history`
- **Stamp database**: `./db-helper.sh db:stamp head`
- **Check if database is up-to-date**: `./db-helper.sh db:check`

### Helper Commands

- **Set up environment**: `./db-helper.sh setup`
- **Tear down environment**: `./db-helper.sh teardown`
- **Show help**: `./db-helper.sh help`

## Common Workflows

### Creating and Applying a Migration

1. Make changes to your SQLAlchemy models (in `models.py`)

2. Generate a migration based on the changes:
   ```bash
   ./db-helper.sh db:auto "Description of changes"
   ```

3. Review the generated migration file in `balancedbrief/app/db/alembic/versions/`

4. Apply the migration:
   ```bash
   ./db-helper.sh db:upgrade head
   ```

### Starting with an Existing Database

If you already have a database schema and want to start using Alembic:

1. Create your SQLAlchemy models to match the existing schema

2. Initialize Alembic:
   ```bash
   ./db-helper.sh db:init
   ```

3. Generate an initial migration:
   ```bash
   ./db-helper.sh db:auto "Initial schema"
   ```

4. Instead of applying the migration (which would try to create tables that already exist), stamp the database:
   ```bash
   ./db-helper.sh db:stamp head
   ```

This tells Alembic that the current database state matches the latest migration.

## Connection Information

When your application needs to connect to the PostgreSQL database:

- **Host**: localhost
- **Port**: 5432
- **User**: postgres
- **Password**: db_pass
- **Database**: postgres

**Connection string**:
```
postgresql://postgres:db_pass@localhost:5432/postgres
```

## Troubleshooting

### Database Connection Issues

- Check if PostgreSQL is running: `./db-helper.sh pg:status`
- View PostgreSQL logs: `./db-helper.sh pg:logs`
- Restart PostgreSQL: `./db-helper.sh pg:stop` then `./db-helper.sh pg:start`

### Alembic Issues

- If you get import errors, make sure your Python path includes your application modules
- Review the generated migration files before applying them
- For complex schema changes, consider creating manual migrations