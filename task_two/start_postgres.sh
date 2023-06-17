#!/bin/bash

if [ "$(docker images -q postgres-bobdb 2> /dev/null)" ]; then
    echo "Образ Docker уже существует"
else
    pip install -r req.txt
    docker build -t postgres-bobdb .
fi

if [ "$(docker ps -aq -f name=postgres-container)" ]; then
    docker start postgres-container
    echo "Контейнер с PostgreSQL уже запущен"
else
    docker run -d -p 5432:5432 --name postgres-container postgres-bobdb
    sleep 5

    echo "Новый контейнер с PostgreSQL создан и запущен"
fi