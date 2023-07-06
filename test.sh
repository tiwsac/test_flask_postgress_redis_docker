#!/bin/bash

docker-compose build && docker-compose run --rm flask bash -c "python3 -m unittest discover tests"