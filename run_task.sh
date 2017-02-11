#!/bin/bash
source /home/canecto/django/venv/bin/activate
python /home/canecto/django/track/manage.py runcrons --force
deactivate