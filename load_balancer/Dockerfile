# This file contains the configuration for building the load balancer container.

FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8080 to match docker-compose and Flask app
EXPOSE 8080

# Command to run the load balancer
CMD ["python", "load_balancer.py"]