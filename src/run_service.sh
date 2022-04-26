#!/bin/bash

python manage.py create_db

gunicorn --preload -w 2 -b 0.0.0.0:8008 manage:app --timeout 7200
