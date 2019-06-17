

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time

@shared_task
def add(x, y):
    print("enter add x={},y={}".format(x,y))
    time.sleep(3)
    return x + y


@shared_task
def mul(x, y):
    print("enter mul x={},y={}".format(x, y))
    time.sleep(3)
    return x * y


@shared_task
def xsum(numbers):
    print("enter xsum numbers={}".format(numbers))
    time.sleep(3)
    return sum(numbers)