#!/bin/bash

cd /code/api/

# run migrations
python3 manage.py db upgrade
