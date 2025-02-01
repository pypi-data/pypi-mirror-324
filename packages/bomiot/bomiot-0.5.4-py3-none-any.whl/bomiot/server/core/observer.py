import inspect
import time
from threading import Thread
import json
import importlib
from django.dispatch import receiver
from bomiot.server.core.signal import bomiot_signals
from django_apscheduler.models import DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from bomiot.server.core.models import JobList
from django.conf import settings

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"File {event.src_path} has been modified")

observer = Observer()
event_handler = MyHandler()


class ObserverManager(Thread):
    """
        Observer of media folder
    """

    def __init__(self, observer):
        """
        init manager
        :param scheduler:
        """
        super(ObserverManager, self).__init__()
        self.observer = observer
        self.observer.start()

    def run(self):
        """
        heart beat detect
        :return:
        """
        self.observer.schedule(event_handler, path=settings.MEDIA_ROOT, recursive=True)


# init observer manager
ob = ObserverManager(observer)
