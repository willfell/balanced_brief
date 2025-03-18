#!/bin/bash
# pg-manage.sh - Script to manage PostgreSQL in Docker for development

# Colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.postgres.yml"
CONTAINER_NAME="balanced_brief_postgres"

# Function to display usage information
usage() {
    echo -e "${YELLOW}Usage:${NC} $0 [start|stop|status|logs|connect|psql|reset|help]"
    echo
    echo "Commands:"
    echo "  start   - Start the PostgreSQL container"
    echo "  stop    - Stop the PostgreSQL container"
    echo "  status  - Show the status of the PostgreSQL container"
    echo "  logs    - Show logs from the PostgreSQL container"
    echo "  connect - Connect to PostgreSQL using psql from host (requires psql client)"
    echo "  psql    - Connect to PostgreSQL using psql inside the container"
    echo "  reset   - Stop container and remove volume (WARNING: DELETES ALL DATA)"
    echo "  help    - Show this help message"
    echo
    echo "Connection Information:"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  User: postgres"
    echo "  Password: db_pass"
    echo "  Database: postgres"
    echo
    echo "Connection String:"
    echo "  postgresql://postgres:db_pass@localhost:5432/postgres"
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
    echo "Check logs with: $0 logs"
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

# Connect to PostgreSQL using psql from host
connect_postgres() {
    if ! command -v psql &> /dev/null; then
        echo -e "${RED}Error: psql is not installed on your host machine${NC}"
        echo "Try using '$0 psql' instead to connect from inside the container"
        return 1
    fi
    
    echo -e "${YELLOW}Connecting to PostgreSQL...${NC}"
    PGPASSWORD=db_pass psql -h localhost -p 5432 -U postgres
}

# Connect to PostgreSQL using psql inside the container
psql_postgres() {
    if [ $(docker ps --filter "name=$CONTAINER_NAME" -q | wc -l) -eq 0 ]; then
        echo -e "${RED}Error: PostgreSQL container is not running${NC}"
        echo "Start it with '$0 start'"
        return 1
    fi
    
    echo -e "${YELLOW}Connecting to PostgreSQL inside the container...${NC}"
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

# Main function
main() {
    check_docker
    
    case "$1" in
        start)
            start_postgres
            ;;
        stop)
            stop_postgres
            ;;
        status)
            status_postgres
            ;;
        logs)
            logs_postgres
            ;;
        connect)
            connect_postgres
            ;;
        psql)
            psql_postgres
            ;;
        reset)
            reset_postgres
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