#!/bin/bash

docker-compose up -d database
sleep 5s
docker-compose exec database bash -c "./load_db.sh"