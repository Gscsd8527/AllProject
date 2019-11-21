from __future__ import absolute_import, unicode_literals
from celery import shared_task

@shared_task
def hello_world():
    with open("output.txt", "a") as f:
        f.write("hello world")
        f.write("\n")
