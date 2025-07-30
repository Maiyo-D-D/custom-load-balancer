#!/bin/bash

# This script sets up the development environment for the load balancer project.

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Python and pip if not already installed
echo "Installing Python and pip..."
sudo apt-get install -y python3 python3-pip

# Install project dependencies
echo "Installing project dependencies..."
pip3 install -r requirements.txt

# Install server dependencies
echo "Installing server dependencies..."
pip3 install -r server/requirements.txt

# Install load balancer dependencies
echo "Installing load balancer dependencies..."
pip3 install -r load_balancer/requirements.txt

echo "Setup complete. You can now run the project."