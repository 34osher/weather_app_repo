#!/bin/bash

echo "starting deployment"

cd /home/ubuntu/deploy/

docker compose down -v
docker rmi -f "$(docker images -aq)"
docker system prune -fa

docker compose up -d --scale flask_app=2