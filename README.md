# Distributed Systems Load Balancer

A scalable, consistent hashing-based load balancer implementation for distributed systems.

## Project Overview

This project implements a customizable load balancer that routes requests from multiple clients asynchronously among several servers using consistent hashing. The load balancer ensures nearly even distribution of load and provides automatic failure recovery.

### Key Features

- **Consistent Hashing**: Uses a 512-slot hash ring with 9 virtual servers per physical server
- **Automatic Scaling**: Add/remove servers dynamically via REST APIs
- **Health Monitoring**: Continuous health checks with automatic failure recovery
- **Container Management**: Full Docker container lifecycle management
- **Load Distribution**: Efficient request routing with minimal redistribution

## Architecture

```text
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Client 1  │────│                  │────│   Server 1  │
└─────────────┘    │                  │    └─────────────┘
│  Load Balancer   │
┌─────────────┐────│  (Port 5000)     │────┌─────────────┐
│   Client 2  │    │                  │    │   Server 2  │
└─────────────┘    │  - Consistent    │    └─────────────┘
│    Hashing       │
┌─────────────┐────│  - Health Check  │────┌─────────────┐
│   Client N  │    │  - Auto Recovery │    │   Server N  │
└─────────────┘    └──────────────────┘    └─────────────┘
```

### Prerequisites

- Ubuntu 20.04 LTS or higher
- Docker 20.10.23 or higher  
- Python 3.9+
- Git

### Installation & Deployment

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd load-balancer-project
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   cd server
   pip install -r requirements.txt
   cd ../load_balancer
   pip install -r requirements.txt
   ```

3. **Run with Docker Compose**:
   ```bash
   docker-compose up
   ```

## Additional Information

- REST APIs allow dynamic scaling and health monitoring.
- Performance analysis scripts and tests are included in the `tests` directory.
- See component-specific README files for more details.
