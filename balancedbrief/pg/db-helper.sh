#!/bin/bash

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.postgres.yml"
CONTAINER_NAME="balanced_brief_postgres"
ALEMBIC_DIR="./balancedbrief/app/db"
ALEMBIC_INI="$ALEMBIC_DIR/alembic.ini"

# PostgreSQL connection settings
PG_HOST="localhost"
PG_PORT="5432"
PG_USER="postgres"
PG_PASSWORD="db_pass"
PG_DATABASE="postgres"

# Function to display usage information
usage() {
    echo -e "${BLUE}Balanced Brief Database Helper${NC}"
    echo -e "============================="
    echo -e "${YELLOW}Usage:${NC} $0 [command]"
    echo
    echo -e "${GREEN}PostgreSQL Commands:${NC}"
    echo "  pg:start     - Start the PostgreSQL container"
    echo "  pg:stop      - Stop the PostgreSQL container"
    echo "  pg:status    - Show the status of the PostgreSQL container"
    echo "  pg:logs      - Show logs from the PostgreSQL container"
    echo "  pg:connect   - Connect to PostgreSQL using psql"
    echo "  pg:reset     - Stop container and remove volume (WARNING: DELETES ALL DATA)"
    echo
    echo -e "${GREEN}Alembic Commands:${NC}"
    echo "  db:init               - Initialize Alembic in your project"
    echo "  db:revision [message] - Create a new empty revision"
    echo "  db:auto [message]     - Create a new auto-generated revision based on model changes"
    echo "  db:upgrade [revision] - Upgrade database to specified revision or 'head'"
    echo "  db:downgrade [rev]    - Downgrade database to specified revision"
    echo "  db:current            - Show current revision"
    echo "  db:history            - Show revision history"
    echo "  db:stamp [revision]   - Stamp the database with the given revision"
    echo "  db:check              - Check if the database is up-to-date with migrations"
    echo
    echo -e "${GREEN}Helper Commands:${NC}"
    echo "  setup      - Start PostgreSQL and prepare for development"
    echo "  teardown   - Stop PostgreSQL and clean up"
    echo "  help       - Show this help message"
    echo
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 setup                    # Set up local development environment"
    echo "  $0 db:auto \"Add user table\" # Generate migration for model changes"
    echo "  $0 db:upgrade head          # Upgrade to latest revision"
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Error: Docker is not installed or not in PATH${NC}"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Error: Docker Compose is not installed or not in PATH${NC}"
        exit 1
    fi
}

# Check Python and Alembic dependencies
check_alembic_dependencies() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: python3 is not installed${NC}"
        exit 1
    fi
    
    if ! command -v alembic &> /dev/null; then
        echo -e "${YELLOW}Installing Alembic...${NC}"
        pip install alembic sqlalchemy psycopg2-binary
    fi
}

# --- PostgreSQL Functions ---

# Start the PostgreSQL container
start_postgres() {
    echo -e "${YELLOW}Starting PostgreSQL container...${NC}"
    docker-compose -f $COMPOSE_FILE up -d
    
    # Wait for PostgreSQL to be ready
    echo -e "${YELLOW}Waiting for PostgreSQL to be ready...${NC}"
    for i in {1..30}; do
        if docker exec $CONTAINER_NAME pg_isready -U postgres &> /dev/null; then
            echo -e "${GREEN}PostgreSQL is ready!${NC}"
            echo -e "${GREEN}Connection details:${NC}"
            echo "  Host: localhost"
            echo "  Port: 5432"
            echo "  User: postgres"
            echo "  Password: db_pass"
            echo "  Database: postgres"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    echo -e "\n${RED}PostgreSQL did not become ready in time.${NC}"
    echo "Check logs with: $0 pg:logs"
    return 1
}

# Stop the PostgreSQL container
stop_postgres() {
    echo -e "${YELLOW}Stopping PostgreSQL container...${NC}"
    docker-compose -f $COMPOSE_FILE down
    echo -e "${GREEN}PostgreSQL container stopped${NC}"
}

# Show status of the PostgreSQL container
status_postgres() {
    echo -e "${YELLOW}PostgreSQL container status:${NC}"
    docker ps --filter "name=$CONTAINER_NAME" --format "table {{.ID}}\t{{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # If no container is running, show a message
    if [ $(docker ps --filter "name=$CONTAINER_NAME" -q | wc -l) -eq 0 ]; then
        echo -e "${RED}PostgreSQL container is not running${NC}"
    fi
}

# Show logs from the PostgreSQL container
logs_postgres() {
    echo -e "${YELLOW}PostgreSQL container logs:${NC}"
    docker logs $CONTAINER_NAME
}

# Connect to PostgreSQL using psql
connect_postgres() {
    if [ $(docker ps --filter "name=$CONTAINER_NAME" -q | wc -l) -eq 0 ]; then
        echo -e "${RED}Error: PostgreSQL container is not running${NC}"
        echo "Start it with '$0 pg:start'"
        return 1
    fi
    
    echo -e "${YELLOW}Connecting to PostgreSQL...${NC}"
    docker exec -it $CONTAINER_NAME psql -U postgres
}

# Reset PostgreSQL (stop container and remove volume)
reset_postgres() {
    echo -e "${RED}WARNING: This will delete ALL PostgreSQL data!${NC}"
    read -p "Are you sure you want to continue? (y/N) " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Stopping PostgreSQL and removing volumes...${NC}"
        docker-compose -f $COMPOSE_FILE down -v
        echo -e "${GREEN}PostgreSQL reset complete${NC}"
    else
        echo -e "${YELLOW}Reset cancelled${NC}"
    fi
}

# --- Alembic Functions ---

# Initialize Alembic
init_alembic() {
    echo -e "${YELLOW}Initializing Alembic...${NC}"
    
    if [ ! -d "$ALEMBIC_DIR" ]; then
        mkdir -p "$ALEMBIC_DIR"
    fi
    
    # Change to the project directory
    cd "$ALEMBIC_DIR"
    
    # Initialize Alembic
    if [ -f "$ALEMBIC_INI" ]; then
        echo -e "${RED}Alembic already initialized (alembic.ini exists)${NC}"
        return 1
    fi
    
    # Run alembic init
    alembic init alembic
    
    # Update the connection string in alembic.ini
    CONNECTION_STRING="postgresql://$PG_USER:$PG_PASSWORD@$PG_HOST:$PG_PORT/$PG_DATABASE"
    sed -i.bak "s|^sqlalchemy.url = .*|sqlalchemy.url = $CONNECTION_STRING|" alembic.ini
    
    echo -e "${GREEN}Alembic initialized successfully${NC}"
    echo -e "${YELLOW}Remember to update env.py to import your SQLAlchemy models${NC}"
}

# Create a new revision
create_revision() {
    local message="$1"
    if [ -z "$message" ]; then
        echo -e "${RED}Error: Revision message is required${NC}"
        echo "Usage: $0 db:revision \"Your revision message\""
        return 1
    fi
    
    echo -e "${YELLOW}Creating new revision: $message${NC}"
    cd "$ALEMBIC_DIR"
    alembic revision -m "$message"
    
    echo -e "${GREEN}Revision created successfully${NC}"
    echo -e "${YELLOW}Edit the newly created file in alembic/versions/ to add your changes${NC}"
}

# Create an auto-generated revision
create_auto_revision() {
    local message="$1"
    if [ -z "$message" ]; then
        echo -e "${RED}Error: Revision message is required${NC}"
        echo "Usage: $0 db:auto \"Your revision message\""
        return 1
    fi
    
    echo -e "${YELLOW}Creating auto-generated revision: $message${NC}"
    cd "$ALEMBIC_DIR"
    alembic revision --autogenerate -m "$message"
    
    echo -e "${GREEN}Auto-generated revision created successfully${NC}"
    echo -e "${YELLOW}Review the generated file in alembic/versions/ before applying${NC}"
}

# Upgrade database
upgrade_database() {
    local revision="${1:-head}"
    
    echo -e "${YELLOW}Upgrading database to revision: $revision${NC}"
    cd "$ALEMBIC_DIR"
    alembic upgrade "$revision"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Database upgraded successfully to $revision${NC}"
    else
        echo -e "${RED}Database upgrade failed${NC}"
        return 1
    fi
}

# Downgrade database
downgrade_database() {
    local revision="$1"
    if [ -z "$revision" ]; then
        echo -e "${RED}Error: Revision is required for downgrade${NC}"
        echo "Usage: $0 db:downgrade <revision>"
        return 1
    fi
    
    echo -e "${YELLOW}Downgrading database to revision: $revision${NC}"
    cd "$ALEMBIC_DIR"
    alembic downgrade "$revision"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Database downgraded successfully to $revision${NC}"
    else
        echo -e "${RED}Database downgrade failed${NC}"
        return 1
    fi
}

# Show current revision
show_current() {
    echo -e "${YELLOW}Current database revision:${NC}"
    cd "$ALEMBIC_DIR"
    alembic current
}

# Show revision history
show_history() {
    echo -e "${YELLOW}Revision history:${NC}"
    cd "$ALEMBIC_DIR"
    alembic history
}

# Stamp database with revision
stamp_database() {
    local revision="${1:-head}"
    
    echo -e "${YELLOW}Stamping database with revision: $revision${NC}"
    cd "$ALEMBIC_DIR"
    alembic stamp "$revision"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Database stamped successfully with $revision${NC}"
    else
        echo -e "${RED}Database stamping failed${NC}"
        return 1
    fi
}

# Check if database is up-to-date
check_database() {
    echo -e "${YELLOW}Checking if database is up-to-date...${NC}"
    cd "$ALEMBIC_DIR"
    
    local curr=$(alembic current 2>/dev/null | awk '{print $1}')
    local head=$(alembic heads 2>/dev/null | awk '{print $1}')
    
    if [ "$curr" = "$head" ]; then
        echo -e "${GREEN}Database is up-to-date (revision: $curr)${NC}"
    else
        echo -e "${RED}Database is not up-to-date${NC}"
        echo "Current revision: $curr"
        echo "Latest revision: $head"
        echo -e "Run '${YELLOW}$0 db:upgrade head${NC}' to update"
    fi
}

# Set up the development environment
setup_dev_environment() {
    echo -e "${BLUE}Setting up development environment...${NC}"
    
    # Start PostgreSQL
    start_postgres
    
    # Check if Alembic is initialized
    if [ ! -f "$ALEMBIC_INI" ]; then
        echo -e "${YELLOW}Alembic not initialized. You may want to run '$0 db:init'${NC}"
    else
        # Check database status
        check_database
    fi
    
    echo -e "${GREEN}Development environment is ready!${NC}"
}

# Tear down the development environment
teardown_dev_environment() {
    echo -e "${BLUE}Tearing down development environment...${NC}"
    
    # Stop PostgreSQL
    stop_postgres
    
    echo -e "${GREEN}Development environment has been torn down${NC}"
}

# Main function
main() {
    check_docker
    
    case "$1" in
        # PostgreSQL commands
        pg:start)
            start_postgres
            ;;
        pg:stop)
            stop_postgres
            ;;
        pg:status)
            status_postgres
            ;;
        pg:logs)
            logs_postgres
            ;;
        pg:connect)
            connect_postgres
            ;;
        pg:reset)
            reset_postgres
            ;;
            
        # Alembic commands
        db:init)
            check_alembic_dependencies
            init_alembic
            ;;
        db:revision)
            check_alembic_dependencies
            create_revision "$2"
            ;;
        db:auto)
            check_alembic_dependencies
            create_auto_revision "$2"
            ;;
        db:upgrade)
            check_alembic_dependencies
            upgrade_database "$2"
            ;;
        db:downgrade)
            check_alembic_dependencies
            downgrade_database "$2"
            ;;
        db:current)
            check_alembic_dependencies
            show_current
            ;;
        db:history)
            check_alembic_dependencies
            show_history
            ;;
        db:stamp)
            check_alembic_dependencies
            stamp_database "$2"
            ;;
        db:check)
            check_alembic_dependencies
            check_database
            ;;
            
        # Helper commands
        setup)
            setup_dev_environment
            ;;
        teardown)
            teardown_dev_environment
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

# Run the main function with all arguments
main "$@"