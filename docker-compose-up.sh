#!/bin/bash


if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose не установлен, устанавливаем..."
    apt-get update
    apt-get install -y docker-compose
fi

sudo docker-compose up --build