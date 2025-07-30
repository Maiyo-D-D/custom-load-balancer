# Makefile for Load Balancer Project

# Define variables
PYTHON=python3
PIP=pip3
DOCKER=docker
COMPOSE=docker-compose

# Define services
SERVICES=server load_balancer

# Default target
all: build

# Build all services
build: 
	@$(COMPOSE) build

# Run all services
run: 
	@$(COMPOSE) up

# Stop all services
stop: 
	@$(COMPOSE) down

# Run tests
test: 
	@$(PYTHON) -m unittest discover -s tests

# Clean up containers and images
clean: 
	@$(DOCKER) system prune -f

# Display help
help:
	@echo "Makefile commands:"
	@echo "  all         - Build all services"
	@echo "  build       - Build services"
	@echo "  run         - Run services (load balancer on :8080, server on :5000)"
	@echo "  stop        - Stop services"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean up containers and images"
	@echo "  help        - Display this help message"