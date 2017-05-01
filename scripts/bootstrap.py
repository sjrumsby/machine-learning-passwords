#!/usr/bin/python

import django
import sys
import os

if "/var/www/django/machienLearning" not in sys.path:
        sys.path.append("/var/www/django/machineLearning")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "machineLearning.settings")
django.setup()

from machineLearning import settings
from main.models import *

import logging
logger = logging.getLogger(__name__)

logger.info("Start bootstrap")

statuses = ["Untrained", "Trained",]

for s in statuses:
    try:
        u = User_Status.objects.get(description=s)
    except User_Status.DoesNotExist:
        u = User_Status.objects.create(description=s)
        u.save()

logger.info("Complete")

