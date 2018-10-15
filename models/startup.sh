#!/bin/bash
python manage.py migrate
python manage.py loaddata db.json
exec "$@"