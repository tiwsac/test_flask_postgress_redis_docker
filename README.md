# backend-engineer-task

## Project Dependencies

- docker
- docker-compose
- bash (optional)

## Setup

- build the project `docker-compose build`
- setup the database using `setup_db.sh` or your own preferred method

## Task Requirements

- implement handlers for routes in app.routes.index
- use the provided postgres database
- - use psycopg2 or an ORM for database queries
- test handlers and aim for maximum test coverage
- implement caching where appropriate

## Remarks

- you can test using `test.sh` or your preferred method
- you're not limited to the packages in the `requirements.txt`, install what you think is appropriate
- if you wish to use an ORM besides psycopg2 you're welcome to, but will have to set up the models yourself
