#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0

python -m gunicorn -w 8 -b 0.0.0.0:8081 \
        --access-logfile - \
        --error-logfile - \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 120 \
        dashboard.wsgi:application
