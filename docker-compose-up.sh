#!/bin/bash

if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose не установлен, устанавливаем..."
    apt-get update
    apt-get install -y docker-compose
fi

if [ "$(docker ps -q -f name=redis)" ]; then
    echo "Redis контейнер уже запущен"
else
    echo "Запускаем Redis контейнер..."
    docker-compose up -d redis
fi

if [ "$(docker ps -q -f name=my-service)" ]; then
    echo "my-service контейнер уже запущен"
else
    echo "Запускаем my-service контейнер..."
    docker-compose up -d my-service
fi