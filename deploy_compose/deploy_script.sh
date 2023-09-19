#!/bin/bash

echo "starting deployment"

cd /home/ubuntu/deploy/

docker compose down -v
docker rmi -fa "$(docker images -aq)"

docker compose up -d --scale flask_app=2