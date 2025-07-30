# Distributed Systems Load Balancer

A scalable, consistent hashing-based load balancer implementation for distributed systems, designed with fault tolerance, dynamic scalability, and observability in mind.

## Project Overview

This project implements a customizable load balancer that routes requests from multiple clients to backend servers using consistent hashing. It supports dynamic scaling, auto recovery, and containerized deployment via Docker.

## Key Features

- Consistent Hashing (512-slot ring, 9 virtual nodes/server)
- Dynamic Scaling via REST API
- Health Monitoring and Auto-Recovery
- Dockerized Deployment
- Comprehensive Testing Framework
- Performance Analysis & Visualization

## Architecture

```text
┌─────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Client 1  │────│                  │────│   Server 1  │
└─────────────┘    │                  │    └─────────────┘
                  │  Load Balancer    │
┌─────────────┐────│   (Port 5000)    │────┌─────────────┐
│   Client 2  │    │                  │    │   Server 2  │
└─────────────┘    │ - Consistent     │    └─────────────┘
                  │    Hashing       │
┌─────────────┐────│ - Health Check   │────┌─────────────┐
│   Client N  │    │ - Auto Recovery  │    │   Server N  │
└─────────────┘    └──────────────────┘    └─────────────┘
```

## Quickstart

### Prerequisites

- Ubuntu 20.04+
- Docker 20.10+
- Python 3.9+
- `make` utility (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Maiyo-D-D/custom-load-balancer.git
   cd custom-load-balancer
   ```

2. Build and run the containers:

   ```bash
   make run
   ```

3. Test deployment:

   ```bash
   make test
   ```

4. View real-time logs:

   ```bash
   make logs
   ```

## REST API Endpoints

| Method | Endpoint    | Description                     |
|--------|-------------|---------------------------------|
| GET    | `/rep`      | Returns status of all servers   |
| POST   | `/add`      | Add a new backend server        |
| DELETE | `/rm`       | Remove a backend server         |
| GET    | `/<path>`   | Route client request dynamically |

## Repository Structure

```
load-balancer-project/
├── README.md
├── Makefile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
│
├── server/
│   ├── server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── load_balancer/
│   ├── load_balancer.py
│   ├── consistent_hash.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── tests/
│   ├── test_server.py
│   ├── test_consistent_hash.py
│   ├── test_load_balancer.py
│   ├── performance_analysis.py
│   └── README.md
│
├── analysis/
│   ├── performance_report.md
│   ├── charts/
│   └── logs/
│
├── docs/
│   ├── design_choices.md
│   ├── api_documentation.md
│   └── troubleshooting.md
│
└── scripts/
    ├── setup.sh
    ├── cleanup.sh
    └── deploy.sh
```

## Design Choices and Rationale

### Overview

This document explains the key design decisions made during the implementation of the distributed load balancer system.

### 1. Consistent Hashing Implementation

**Choice:** Circular Hash Ring with Virtual Servers

**Rationale:**

- Minimizes data movement when servers are added/removed
- Ensures even load distribution across all servers
- Virtual servers (9 per physical server) improve load balancing quality

**Hash Functions:**

- **Request Mapping:** `H(i) = i² + 2i + 17`
  - Quadratic function provides good distribution
  - Prime constant (17) reduces clustering
  - Simple computation for fast request routing
- **Virtual Server Mapping:** `Φ(i,j) = i² + j² + 2j + 25`
  - Incorporates both server ID and virtual replica ID
  - Different formula from request mapping prevents correlation
  - Ensures virtual servers are well-distributed across the ring

**Alternatives Considered:**

- Linear Hash Functions: Rejected due to poor distribution
- Cryptographic Hashes: Rejected due to performance overhead
- Multiplicative Hashing: Good alternative, but current functions are sufficient

### 2. Container Management Architecture

**Choice:** Privileged Containers with Docker Socket Sharing

**Rationale:**

- Allows load balancer to spawn/manage server containers
- Provides full control over container lifecycle
- Enables dynamic scaling operations

**Security Considerations:**

- Privileged containers pose security risks in production
- Suitable for educational/controlled environments
- Production deployment would use orchestration platforms (Kubernetes)

**Alternatives Considered:**

- External Orchestrator: Would require additional complexity
- Pre-spawned Container Pool: Less flexible for dynamic scaling

### 3. Health Monitoring System

**Choice:** Periodic Heartbeat Checks with Automatic Recovery

**Rationale:**

- Detects failures within 10-15 seconds
- Automatically maintains desired server count
- Minimal overhead on system performance

**Parameters:**

- Check interval: 10 seconds
- Timeout: 5 seconds
- Recovery delay: 2 seconds

**Alternatives Considered:**

- Event-based Monitoring: More complex to implement
- Shorter Intervals: Would increase system overhead

### 4. API Design

**Choice:** RESTful API with JSON Payloads

**Rationale:**

- Standard HTTP methods (GET, POST, DELETE)
- JSON format for structured data exchange
- Clear error handling with appropriate status codes

**Endpoint Design:**

- `/rep`: Status information (GET only)
- `/add`: Server addition (POST with payload)
- `/rm`: Server removal (DELETE with payload)
- `/<path>`: Request routing (GET for any path)

**Validation Strategy:**

- Input sanitization for all payloads
- Hostname length validation
- Numeric parameter bounds checking
- Graceful error responses

### 5. Threading and Concurrency

**Choice:** Background Health Check Thread

**Rationale:**

- Non-blocking health monitoring
- Flask main thread handles requests
- Daemon thread for automatic cleanup

**Thread Safety:**

- Shared state protection using appropriate locking
- Atomic operations for critical sections
- Minimal lock contention for performance

### 6. Error Handling and Resilience

**Strategy:** Graceful Degradation

- Failed server spawning doesn't crash system
- Invalid requests return meaningful errors
- System maintains functionality with reduced capacity

**Logging Strategy:**

- Comprehensive logging at INFO and ERROR levels
- Structured log messages for debugging
- Separate log files for different components

### 7. Performance Optimizations

**Request Routing Optimization:**

- Pre-computed hash values where possible
- Efficient ring traversal algorithm
- Minimal string operations in hot paths

**Memory Management:**

- Fixed-size hash ring array
- Efficient data structures for server metadata
- Minimal object creation in request handling

### 8. Testing Strategy

**Multi-layer Testing Approach:**

- Unit Tests: Individual component validation
- Integration Tests: End-to-end functionality
- Load Tests: Performance under stress
- Failure Tests: Recovery scenarios

**Analysis Framework:**

- Automated performance analysis
- Statistical load distribution analysis
- Visual representation of results
- Comparative analysis of different configurations

### 9. Deployment Considerations

**Development vs Production:**

**Current Implementation (Development):**

- Single-host Docker deployment
- Privileged containers
- Direct container management

**Production Recommendations:**

- Kubernetes orchestration
- Service mesh for networking
- External health monitoring
- Horizontal pod autoscaling

### 10. Scalability Considerations

**Current Limitations:**

- Single load balancer instance (SPOF)
- Host resource constraints
- Docker socket dependency

**Scaling Solutions:**

- Load balancer clustering
- Distributed consistent hashing
- External service discovery
- Cloud-native deployment