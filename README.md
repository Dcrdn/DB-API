# DB-API

Backend of the final project of my Advanced Databases lecture at ITESM Gda. 2019

You need to have created a DB in postgreSQL. 
You need to know your user, password and name of the DB.

## Install the requirements

- pip install

## Run on terminal where you will run your code (change parameters with your user, password and DB name)

export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql://PostgressUser:PostgresPassword@localhost/PostgresDatabase"

## It can work just by running:
- python manage.py runserver

## Another option:
- python manage.py db init
- python manage.py db migrate
- python manage.py db upgrade
- python manage.py runserver

## Endpoints
- All the endpoints are GET methods that receive a parameter named "username" which is the username of the user on twitter.

- /sentimientos
- /hashtags
- /dates
- /commonWords
- /dias
