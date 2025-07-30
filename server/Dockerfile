FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Create log directory if needed
RUN mkdir -p /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Expose port 5000
EXPOSE 5000

# Command to run the server
CMD ["python", "server.py"]