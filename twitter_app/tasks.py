from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def test_task(a, b):
    time.sleep(5)
    return a + b