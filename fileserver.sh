#!/bin/sh

docker network create default-network

docker volume create servervol
docker volume create data

docker build -t server:1 ./server
docker build -t mongodb:1 ./database

docker container rm mongodb
docker container rm server
docker run --network default-network -v data:/app/data --name mongodb -d mongodb:1
echo "MongoDb is run successfully"

docker run --network default-network -v servervol:/app/serverdata --name server -t server:1
