# API Documentation

## Overview

This document provides detailed information about the API endpoints available in the load balancer project. It includes the request and response formats, as well as examples for each endpoint.

## Base URL

The base URL for accessing the API is:

```
http://<your-server-address>:<port>
```

## Endpoints

### 1. Load Balancer Endpoint

#### Request

- **Method:** `GET`
- **URL:** `/load`
- **Description:** Distributes incoming requests to available server instances.

#### Response

- **Status Code:** `200 OK`
- **Content:**
  - `server_id`: The ID of the server that handled the request.
  - `data`: The response data from the server.

#### Example

**Request:**
```
GET /load HTTP/1.1
Host: <your-server-address>
```

**Response:**
```json
{
  "server_id": "server_1",
  "data": {
    "message": "Hello from server 1!"
  }
}
```

### 2. Health Check Endpoint

#### Request

- **Method:** `GET`
- **URL:** `/health`
- **Description:** Checks the health status of the load balancer.

#### Response

- **Status Code:** `200 OK`
- **Content:**
  - `status`: The health status of the load balancer.

#### Example

**Request:**
```
GET /health HTTP/1.1
Host: <your-server-address>
```

**Response:**
```json
{
  "status": "healthy"
}
```

## Error Handling

In case of an error, the API will return an appropriate status code along with a message describing the error.

### Common Error Responses

- **400 Bad Request:** The request was invalid.
- **404 Not Found:** The requested resource was not found.
- **500 Internal Server Error:** An unexpected error occurred on the server.

## Conclusion

This API documentation provides a comprehensive overview of the available endpoints in the load balancer project. For further details on implementation and usage, please refer to the project's README and other documentation files