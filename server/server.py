#!/usr/bin/env python3
"""
Distributed Systems Assignment 1 - Server Implementation
Task 1: Simple web server with home and heartbeat endpoints

This module implements a lightweight Flask-based web server that:
1. Responds to /home requests with server identification
2. Provides /heartbeat endpoint for health monitoring
3. Runs in Docker containers managed by the load balancer

Author: Leon Bundi
"""

from flask import Flask, jsonify
import os
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/server.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Get server ID from environment variable with fallback
SERVER_ID = os.environ.get('SERVER_ID', 'unknown')
logger.info(f"Server starting with ID: {SERVER_ID}")

@app.route('/home', methods=['GET'])
def home():
    """
    Home endpoint that returns server identification.
    
    Returns:
        JSON response containing:
        - message: Hello message with server ID
        - status: Success indicator
        
    Response Code: 200
    """
    try:
        response_data = {
            "message": f"Hello from Server: {SERVER_ID}",
            "status": "successful"
        }
        logger.info(f"Home request served by Server: {SERVER_ID}")
        return jsonify(response_data), 200
    except Exception as e:
        logger.error(f"Error in home endpoint: {str(e)}")
        return jsonify({
            "message": "Internal server error",
            "status": "failure"
        }), 500

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    """
    Heartbeat endpoint for health monitoring.
    
    Used by the load balancer to check if this server instance
    is alive and responsive.
    
    Returns:
        Empty response with 200 status code
    """
    try:
        logger.debug(f"Heartbeat check for Server: {SERVER_ID}")
        return '', 200
    except Exception as e:
        logger.error(f"Error in heartbeat endpoint: {str(e)}")
        return '', 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response."""
    return jsonify({
        "message": "Endpoint not found",
        "status": "failure"
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with JSON response."""
    return jsonify({
        "message": "Internal server error",
        "status": "failure"
    }), 500

if __name__ == '__main__':
    logger.info(f"Starting server {SERVER_ID} on port 5000")
    
    # Run Flask application
    # host='0.0.0.0' allows external connections
    # debug=False for production deployment
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=False,
        threaded=True  # Enable threading for concurrent requests
    )