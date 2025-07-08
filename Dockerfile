FROM python:3.14.0b3-slim

WORKDIR /app

COPY . .

CMD ["python3", "hashing.py"]