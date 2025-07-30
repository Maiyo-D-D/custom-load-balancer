# Load Balancer Documentation

This README file provides specific documentation for the load balancer component of the project. 

## Overview

The load balancer is responsible for distributing incoming requests to multiple server instances, ensuring efficient resource utilization and improved response times.

## Setup Instructions

1. **Clone the Repository**: 
   ```bash
   git clone <repository-url>
   cd load-balancer-project/load_balancer
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

## Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your branch and create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.