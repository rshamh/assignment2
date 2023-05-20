#!/bin/sh

docker volume create clientvol

docker build -t client ./client

docker container rm client
docker run --network default-network -v clientvol:/app/clientdata --name client -t client

docker exec client -it sh