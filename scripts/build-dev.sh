#!bin/sh -c

docker-compose -f docker-compose.dev.yml up --build -d
docker-compose -f docker-compose.dev.yml down