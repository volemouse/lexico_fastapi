#!/bin/bash

docker build -t postgres-bobdb .

docker run -d -p 5432:5432 --name postgres-container postgres-bobdb

# Ожидание, чтобы контейнер успел запуститься
sleep 5

echo "Контейнер запущен и готов к использованию"