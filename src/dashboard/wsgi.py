"""
WSGI config for stats_linebot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dashboard.configs.dev")

"""
python -m gunicorn -w 8 -b 0.0.0.0:8081 \
        --access-logfile - \
        --error-logfile - \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --timeout 120 \
        dashboard.wsgi:application

How dashboard.wsgi:application works? :
    When we open the service with gunicorn,
    gunicorn will find the wsgi.py file, and find the callable WSGI module,
    its name was called application
"""


application = get_wsgi_application()
