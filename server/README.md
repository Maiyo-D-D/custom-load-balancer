# Server Implementation Documentation

This README file provides documentation specific to the server implementation of the load balancer project. It includes setup instructions, usage guidelines, and contribution details.

## Overview

The server is responsible for handling incoming requests and processing them according to the application's logic. It works in conjunction with the load balancer to efficiently distribute requests across multiple server instances.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Maiyo-D-D/custom-load-balancer
   cd custom-load-balancer/server
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Build the Docker Image**
   If you are using Docker, build the server container:
   ```bash
   docker build -t server-image .
   ```

## Usage

To run the server application, execute the following command:
```bash
python server.py
```

If using Docker, you can run the container with:
```bash
docker run -p <host-port>:<container-port> server-image
```