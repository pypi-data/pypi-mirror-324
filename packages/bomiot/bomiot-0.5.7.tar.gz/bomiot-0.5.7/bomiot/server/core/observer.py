from threading import Thread
from django.conf import settings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_deleted(self, event):
        print(f"File {event} on_deleted")

    def on_created(self, event):
        print(f"File {event} on_modified")

observer = Observer()
event_handler = MyHandler()

class ObserverManager(Thread):
    """
        Observer of media folder
    """

    def __init__(self, observer):
        """
        init manager
        :param observer:
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
