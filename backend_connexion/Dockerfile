FROM python:3.11-slim-bullseye
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get upgrade -y && apt-get clean && \
    pip install --upgrade pip && \
    pip install --no-cache-dir connexion[swagger-ui,flask]==2.14.2 && \
    pip install --no-cache-dir -r requirements.txt
COPY . .
COPY .env .env
#COPY cert.pem /app/cert.pem
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:application"]
