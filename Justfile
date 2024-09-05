# Justfile for Django Development

# Set environment variables
set dotenv-load := true  # Load environment variables from a .env file


initialize:
    python manage.py makemigrations
    python manage.py migrate
    python manage.py load_initial_state

# Basic Django commands

# Install dependencies
install:
    @echo "Installing dependencies..."
    poetry install

lock:
    @echo "Locking dependencies..."
    poetry lock && poetry install --with dev --sync

# Run the Django development server
serve:
    @echo "Starting Django development server..."
    python manage.py runserver

# Run Django shell
shell:
    @echo "Opening Django shell..."
    python manage.py shell

# Create and apply migrations
migrate:
    @echo "Making migrations..."
    python manage.py makemigrations
    @echo "Applying migrations..."
    python manage.py migrate

# Load initial data for the game from TOML file
load:
    @echo "Loading initial game state from TOML..."
    python manage.py load_initial_state

# Create a superuser
superuser:
    @echo "Creating a Django superuser..."
    python manage.py createsuperuser

# Collect static files
collectstatic:
    @echo "Collecting static files..."
    python manage.py collectstatic --noinput

# Development commands

# Run tests
test:
    @echo "Running tests..."
    python manage.py test

# Run linting using flake8
lint:
    @echo "Linting code with flake8..."
    pylint .

# Run formatting using black
format:
    @echo "Formatting code with black..."
    black .

# Run type checks with mypy
typecheck:
    @echo "Checking types with mypy..."
    mypy adventure_game

# Check for security vulnerabilities with bandit
security:
    @echo "Running security checks with bandit..."
    bandit -r adventure_game

# Run all checks (lint, format, type checks, tests)
check:
    @echo "Running all checks (lint, format, type checks, tests)..."
    just lint
    just format
    just typecheck
    just test

# Clean up __pycache__ files
clean:
    @echo "Cleaning up __pycache__ files..."
    find . -name "__pycache__" -exec rm -rf {} +

# Create and apply database migrations
reset-db:
    @echo "Resetting the database..."
    python manage.py flush --noinput
    just migrate
    just load
