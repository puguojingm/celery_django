from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_django.settings')

app = Celery('celery_django')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


from celery.schedules import crontab
from datetime  import timedelta


app.conf.beat_schedule = {
    'xsum-every-30-seconds': {
        'task': 'apps.app1.tasks.xsum',
        'schedule': timedelta(seconds=10),
        'args': ([1,2,3,4],),
        'options':{
            'queue':'beat_queue'
        }
    },
    'add_time_task': {
        'task': 'apps.app1.tasks.mul',
        'schedule': crontab(hour=1, minute=9),# crontab(hour=4, minute=30, day_of_week=1),每周一早上4：30执行report函数
        'args': (5,6)
    }

}

"""
timedelta是datetime中的一个对象，需要from datetime import timedelta引入，有如下几个参数

days：天

seconds：秒

microseconds：微妙

milliseconds：毫秒

minutes：分

hours：小时

crontab的参数有：

month_of_year：月份

day_of_month：日期

day_of_week：周

hour：小时

minute：分钟
"""

app.conf.timezone = "Asia/Shanghai"

from kombu import Queue,Exchange
app.conf.task_queues = (
    Queue('default',Exchange('default'), routing_key='default'),
    Queue('add_queue', Exchange('add_queue'),routing_key='add_queue'),
    Queue('mul_queue', Exchange('mul_queue'),routing_key='mul_queue'),
    Queue('beat_queue', Exchange('beat_queue'),routing_key='beat_queue'),
)

app.conf.task_routes = {
    'apps.app1.tasks.add': {'queue': 'add_queue'},
    'apps.app1.tasks.mul': {'queue': 'mul_queue'},
}

#改变默认的queue名字
app.conf.task_default_queue = 'default'