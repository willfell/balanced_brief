#!/bin/bash
# setup-local.sh

set -e

# Print heading
print_heading() {
    echo "===================================================="
    echo "  $1"
    echo "===================================================="
}

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Check for required environment variables
check_env_vars() {
    local missing=0
    
    if [ -z "$REDDITCLIENTID" ]; then
        echo "REDDITCLIENTID is not set"
        missing=1
    fi
    
    if [ -z "$REDDITCLIENTSECRET" ]; then
        echo "REDDITCLIENTSECRET is not set"
        missing=1
    fi
    
    if [ -z "$REDDITAGENT" ]; then
        echo "REDDITAGENT is not set"
        missing=1
    fi
    
    if [ -z "$OPENAI_KEY" ]; then
        echo "OPENAI_KEY is not set"
        missing=1
    fi
    
    if [ $missing -eq 1 ]; then
        echo "Please set the required environment variables"
        exit 1
    fi
}

# Initialize the local environment
init_environment() {
    print_heading "Setting up local environment"
    
    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        echo "Creating .env file"
        cat > .env << EOF
REDDITCLIENTID=$REDDITCLIENTID
REDDITCLIENTSECRET=$REDDITCLIENTSECRET
REDDITAGENT=$REDDITAGENT
OPENAI_KEY=$OPENAI_KEY
EOF
    fi
}

# Build and start the Docker containers
start_containers() {
    print_heading "Starting containers"
    
    echo "Building and starting containers..."
    docker-compose up -d postgres
    
    echo "Waiting for PostgreSQL to be ready..."
    sleep 5
    
    echo "Running migrations..."
    docker-compose up migrations
    
    echo "Starting application..."
    docker-compose up -d app
    
    echo "Containers started successfully!"
}

# Main function
main() {
    print_heading "Balanced Brief Local Setup"
    
    check_docker
    check_env_vars
    init_environment
    start_containers
    
    print_heading "Setup complete!"
    echo "PostgreSQL is running at: localhost:5432"
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
}

# Run the main function
main