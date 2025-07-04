FROM python:3.13-slim-buster AS builder

WORKDIR /app

# Install pip dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM ubuntu/python:3.13-25.04_stable

WORKDIR /app

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python", "server.py"]