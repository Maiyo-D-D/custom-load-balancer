#!/bin/bash

# This script automates the deployment of the load balancer project.

# Step 1: Build the Docker images
echo "Building Docker images..."
docker-compose build

# Step 2: Start the services
echo "Starting services..."
docker-compose up -d

# Step 3: Run any necessary migrations or setup tasks
# Uncomment and modify the following line if migrations are needed
# docker-compose run web python manage.py migrate

# Step 4: Verify that the services are running
echo "Verifying services..."
docker-compose ps

echo "Deployment completed successfully."