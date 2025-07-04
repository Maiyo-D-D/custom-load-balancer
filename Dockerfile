FROM ubuntu/python:3.13-25.04_stable

WORKDIR /app

RUN pip install flask

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["python", "server.py"]