#!/bin/bash

# Cleanup script for the load balancer project

# Stop and remove Docker containers
docker-compose down

# Remove temporary files and directories
rm -rf ./load_balancer/__pycache__
rm -rf ./server/__pycache__
rm -rf ./tests/__pycache__
rm -rf ./analysis/logs/*
rm -rf ./analysis/charts/*

echo "Cleanup completed."