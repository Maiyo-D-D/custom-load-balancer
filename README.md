# Customizable Load Balancer using Consistent Hashing

## Overview

This project implements a customizable load balancer using **consistent hashing** in a distributed system. It asynchronously distributes client requests among multiple server replicas. It is containerized using Docker and managed through a central load balancer service.

---

## Architecture

- **Load Balancer**: Manages routing, server scaling, and failure recovery.
- **Web Servers**: Simple Flask servers that respond to HTTP GET requests.
- **Consistent Hashing**: Ensures even distribution of requests using virtual nodes.
- **Docker Network**: All components run in isolated containers inside a Docker bridge network.

       +---------+             +-------------+
       | Client  | --------->  | LoadBalancer|
       +---------+             +-------------+
                                |     |      |
                                V     V      V
                        +--------+ +--------+ +--------+
                        | Server1| | Server2| | Server3|
                        +--------+ +--------+ +--------+

---

## Setup

### Requirements

- Docker Desktop (WSL 2 enabled for Windows)
- Docker Compose v2.15+
- Python 3.9+
- Git

### Clone and Run

```bash
git clone https://github.com/Maiyo-D-D/custom-load-balancer.git
cd custom-load-balancer
docker-compose up --build -d

```

### Setting up the dev environment

### Docker installationn on Ubuntu

```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

---
