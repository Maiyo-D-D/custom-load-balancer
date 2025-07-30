# Load Balancer Documentation

This README file provides specific documentation for the load balancer component of the project. 

## Overview

The load balancer is responsible for distributing incoming requests to multiple server instances, ensuring efficient resource utilization and improved response times.

## Setup Instructions

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/Maiyo-D-D/custom-load-balance
   cd custom-load-balancer/load_balancer
   ```

2. **Install Dependencies**: 
   Ensure you have Python and pip installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the Docker Image**: 
   To build the load balancer Docker image, run:
   ```bash
   docker build -t load_balancer .
   ```

## Usage

To run the load balancer, you can use the following command:
```bash
python load_balancer.py
```
Make sure that the server instances are running and accessible.