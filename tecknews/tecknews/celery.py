# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from celery import shared_task

# # set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dockerexample.settings')

# app = Celery('dockerexample')

# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()

import os
from celery import Celery
from time import sleep
from celery.schedules import crontab


# from .tasks import simple_task_1

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tecknews.settings')
app = Celery('tecknews', broker="pyamqp://rabbitmq:5672")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs) -> None:
    # Example of periodic task (will be executed every 30 seconds)
    sender.add_periodic_task(
                        crontab(minute=0, hour=0)
                        , periodic_task.s(),
                        name='Periodic task example')
    


@app.task(name="PeriodicTask (every day midnight)")
def periodic_task() -> None:
    from myscrapy.views import peridic_scrapy
    # simple_task_1.delay()
    peridic_scrapy()
    print("Example of periodic task executed!")


@app.task(name="SimpleTask1", queue="queue1")
def simple_task_1() -> None:
    for i in range(10):
        sleep(0.5)
        print(f"Simple Task 1: {i}")























# from celery import Celery
# # docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3-management


# app = Celery(
#     'celery_app',
#     # broker='amqp://rabbit',
#     broker = "amqp://localhost:5672/",
    
#     # backend='rpc://',

#     # This should include modules/files that define tasks. This is a list of strs 
#     # to be evaluated later in order to get around circular dependencies, I suspect.
#     include=[  
#         'tecknews.tasks',  # This is our file containing our task
#     ]
# )

# # Optional configuration, see the application user guide.
# app.conf.update(result_expires=3600)


# if __name__ == '__main__':
#     app.start()