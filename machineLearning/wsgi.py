"""
WSGI config for machineLearning project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

django_path = "/var/www/django/machineLearning"

if django_path not in sys.path:
        sys.path.append(django_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "machineLearning.settings")

application = get_wsgi_application()
