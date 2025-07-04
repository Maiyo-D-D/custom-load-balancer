FROM python:3.14.0b3-slim

WORKDIR /app

# Install pip dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python3", "server.py"]