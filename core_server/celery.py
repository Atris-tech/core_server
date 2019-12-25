from __future__ import absolute_import, unicode_literals
import os
from celery import Celery


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'core_server.settings'
)
os.environ.setdefault(
    'FORKED_BY_MULTIPROCESSING',
    '1'
)

app = Celery('core_server')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))