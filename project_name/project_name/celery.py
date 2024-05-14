import os
from celery import Celery
# from celery.schedules import crontab
import logging

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

app = Celery('project_name')

app.config_from_object('django.conf:settings', namespace='CELERY')

# from celery.signals import setup_logging
# @setup_logging.connect
# def config_loggers(*args, **kwags):
#     from logging.config import dictConfig
#     from django.conf import settings
#     dictConfig(settings.LOGGING)


# from celery.signals import after_setup_task_logger
# @after_setup_task_logger.connect
# def setup_task_logger(logger, *args, **kwargs):
#     logger.addHandler(logging.StreamHandler())
#     logger.setLevel(logging.INFO)  # Set the desired log level


app.autodiscover_tasks()




@app.task(bind=True, ignore_result=True)
def debug_task(self):
    # print(f'Request: {self.request!r}')
    print("Debugggggggggggggggggggggggggggggggggggggggggggggggggggggg")