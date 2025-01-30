#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print status messages
print_status() {
    echo -e "${GREEN}[+]${NC} $1"
}

print_error() {
    echo -e "${RED}[!]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to prompt yes/no questions
prompt_yes_no() {
    while true; do
        read -p "$1 [y/N] " yn
        case $yn in
            [Yy]* ) return 0;;
            [Nn]* | "" ) return 1;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

# Check if we're on Ubuntu/Debian
check_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]]; then
            return 0
        fi
    fi
    return 1
}

# Check if PostgreSQL container exists and is running
check_postgres_container() {
    if docker ps -a --format '{{.Names}}' | grep -q "automagik-dev-automagik-db-"; then
        if docker ps --format '{{.Names}}' | grep -q "automagik-dev-automagik-db-"; then
            return 0  # Container exists and is running
        else
            return 2  # Container exists but is not running
        fi
    else
        return 1  # Container does not exist
    fi
}

# Function to handle database setup
setup_database() {
    # First check for existing database containers (both dev and prod)
    DB_CONTAINER=""
    if docker ps -a | grep -q "automagik.*db.*"; then
        # Get the actual container ID and name
        CONTAINER_INFO=$(docker ps -a | grep "automagik.*db.*" | grep "postgres" | head -n 1)
        DB_CONTAINER=$(echo "$CONTAINER_INFO" | awk '{print $1}')
        DB_NAME=$(echo "$CONTAINER_INFO" | awk '{print $NF}')
        
        if [[ "$DB_NAME" == *"dev"* ]]; then
            print_warning "Development database container exists ($DB_NAME)"
        else
            print_warning "Production database container exists ($DB_NAME)"
            if prompt_yes_no "Would you like to use the production database? (Recommended only for testing)"; then
                if ! docker ps -q | grep -q "$DB_CONTAINER"; then
                    print_status "Starting production database..."
                    docker start $DB_CONTAINER
                fi
                print_status "Using production database"
                return 0
            fi
        fi
        
        if prompt_yes_no "Would you like to reset the database? (This will delete all data)"; then
            print_status "Stopping database container..."
            docker stop $DB_CONTAINER
            print_status "Removing container and volume..."
            docker rm -f $DB_CONTAINER
            
            # Remove any postgres volumes
            for volume in $(docker volume ls -q | grep "automagik.*postgres"); do
                docker volume rm -f $volume
            done
            
            # Wait for port to be released
            while lsof -i:15432 >/dev/null 2>&1; do
                sleep 1
            done
        else
            print_error "Cannot continue with existing database. Please remove it first."
            exit 1
        fi
    fi

    # Now check if port is in use by something else
    if lsof -i:15432 >/dev/null 2>&1; then
        print_error "PostgreSQL port 15432 is in use by another process."
        print_error "Please free up port 15432 before continuing."
        exit 1
    fi

    print_status "Starting fresh PostgreSQL container..."
    docker compose -p automagik-dev -f docker/docker-compose.dev.yml up -d automagik-db

    # Wait for PostgreSQL to be ready
    print_status "Waiting for PostgreSQL to be ready..."
    local max_retries=30
    local retry_count=0
    local pg_ready=false

    while [ $retry_count -lt $max_retries ]; do
        if pg_isready -h localhost -p 15432 >/dev/null 2>&1; then
            pg_ready=true
            break
        fi
        echo -n "."
        sleep 2
        retry_count=$((retry_count + 1))
    done
    echo "" # New line after dots

    if [ "$pg_ready" = false ]; then
        print_error "PostgreSQL failed to start. Please check docker logs for more information."
        docker compose -p automagik-dev -f docker/docker-compose.dev.yml logs automagik-db
        exit 1
    fi
}

# Check if Python 3.10 or higher is installed
PYTHON_VERSION=$(python3 -c 'import sys; print("".join(map(str, sys.version_info[:2])))' 2>/dev/null || echo "0")
if [ "$PYTHON_VERSION" = "0" ] || [ "$PYTHON_VERSION" -lt "310" ]; then
    print_warning "Python 3.10 or higher is required but not found."
    
    # Check if we can offer automatic installation
    if check_os; then
        if prompt_yes_no "Would you like to install Python 3.10?"; then
            print_status "Installing Python 3.10..."
            # Add deadsnakes PPA for Python 3.10
            if ! command -v add-apt-repository &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y software-properties-common
            fi
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
        else
            print_error "Python 3.10 is required. Please install it manually."
            exit 1
        fi
    else
        print_error "Automatic Python installation is only supported on Ubuntu and Debian."
        print_error "Please install Python 3.10 manually."
        exit 1
    fi
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_warning "uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to PATH for current session if not already there
    if [[ ":$PATH:" != *":$HOME/.cargo/bin:"* ]]; then
        export PATH="$HOME/.cargo/bin:$PATH"
    fi
fi

# Check if docker and docker compose are installed
if ! command -v docker &> /dev/null; then
    print_error "docker is not installed. Please install it first."
    exit 1
fi

if ! command -v docker compose &> /dev/null; then
    print_error "docker compose is not installed. Please install it first."
    exit 1
fi

# Create .env file from example
if [ -f .env ]; then
    if prompt_yes_no "An existing .env file was found.\nWould you like to create a new one? (This will overwrite the existing file)"; then
        cp .env.dev .env
        # Ensure DATABASE_URL is set correctly for local development
        sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://automagik:automagik@localhost:15432/automagik|' .env
        # Ensure worker log path is set correctly
        sed -i 's|^AUTOMAGIK_WORKER_LOG=.*|AUTOMAGIK_WORKER_LOG=logs/worker.log|' .env
        print_status "Environment file created successfully!"
    else
        print_status "Using existing .env file."
        # Ensure DATABASE_URL is set correctly
        if ! grep -q "^DATABASE_URL=postgresql\+asyncpg://automagik:automagik@localhost:15432/automagik" .env; then
            sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://automagik:automagik@localhost:15432/automagik|' .env
            print_status "Updated DATABASE_URL in .env"
        fi
        # Ensure worker log path is set correctly
        if ! grep -q "^AUTOMAGIK_WORKER_LOG=logs/worker.log" .env; then
            sed -i 's|^AUTOMAGIK_WORKER_LOG=.*|AUTOMAGIK_WORKER_LOG=logs/worker.log|' .env
            print_status "Updated AUTOMAGIK_WORKER_LOG in .env"
        fi
    fi
else
    cp .env.dev .env
    # Ensure DATABASE_URL is set correctly
    sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql+asyncpg://automagik:automagik@localhost:15432/automagik|' .env
    # Ensure worker log path is set correctly
    sed -i 's|^AUTOMAGIK_WORKER_LOG=.*|AUTOMAGIK_WORKER_LOG=logs/worker.log|' .env
    print_status "Environment file created successfully!"
fi

# Export environment variables
set -a
source .env
set +a

print_status "Creating logs directory..."
mkdir -p "$(dirname "$AUTOMAGIK_WORKER_LOG")"
touch "$AUTOMAGIK_WORKER_LOG"

print_status "Creating virtual environment..."
uv venv
source .venv/bin/activate

print_status "Checking PostgreSQL availability..."
setup_database

print_status "Installing dependencies..."
uv pip install -e ".[dev]"

print_status "Applying database migrations..."
if ! alembic upgrade head; then
    print_error "Database migration failed. Please check the error above."
    exit 1
fi

print_status "Setting up git hooks..."
if [ -d .githooks ]; then
    git config core.hooksPath .githooks
    chmod +x .githooks/*
    print_status "Git hooks installed successfully!"
else
    print_warning ".githooks directory not found, skipping git hooks setup..."
fi

# Print ASCII art
cat << "EOF"
       ██            ███████████  ████████   ███        ███     █       ▓███████ ░██▓ ███   ████    
       ███   ▓██     ██          ███    ▒██░ ████      ████    ███     ███        ██  ██▒  ███      
      ████    ██     ██   ███   ██        ██ █████    █████   █████   ███  █████  ██  ██  ██▒       
     ▓██ ██   ██     ██   ███   ██   ██▓  ██ ██ ███  ███ ██   ██ ██   ███  █████  ██  █████         
     ██  ███  ██     ██   ███   ███      ░██ ██  ██  ██ ███  ██▒  ██  ███     ██  ██  ███░███       
    ██░   ██  ████▒████   ███    ████  ████  ██   ████      ███   ███  █████ ▓██  ██  █▓   ███░     
   ███    ███   █████     ███      ██████    ██▒   ██      ███░    ███   ▓████████████       ███    
                           
                                    Development Environment Setup
EOF

print_status "Setup completed successfully! 🎉"
print_status "To start developing:"
print_status "1. Run the API: automagik api"
print_status "2. Access services at:"
print_status "   - API: http://localhost:8888"
print_status "   - PostgreSQL: localhost:15432"
