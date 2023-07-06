#!/bin/bash

export PGPASSWORD=password
psql -U postgres -c "CREATE DATABASE app"
PGPASSWORD=password pg_restore -U postgres -d app dump.sql