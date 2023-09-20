from __future__ import absolute_import  , unicode_literals

import os

from celery import Celery

os.environ("DJANGO_SETTING_MODULE" , "config.django.base")

app = Celery("styleguide_example")

app.config_from_object("django.conf:settings" , namespace="CELERY")

app.autodiscover_tasks()