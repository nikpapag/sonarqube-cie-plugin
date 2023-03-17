FROM python:3.9.9-alpine3.14
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod -R 777 /app


CMD ["python3", "/app/main.py"]

