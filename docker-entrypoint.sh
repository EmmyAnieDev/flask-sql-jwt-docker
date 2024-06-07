#!/bin/sh

flask db upgrade

# Start the Gunicorn server with your Flask app
exec gunicorn --bind 0.0.0.0: "main:create_app()"