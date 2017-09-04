import threading


class EjectorThread(object):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        self._args = args
        self._kwargs = kwargs if kwargs else {}
        self._target = target

        if name:
            self._thread = threading.Thread(name=name, target=self._run)
        else:
            self._thread = threading.Thread(target=self._run)

    def __getattr__(self, attr):
        return getattr(self._thread, attr)

    def _run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
            else:
                self.run()
        except:
            # crash_logger.exception('UNHANDLED EXCEPTION in thread: {0}'.format(self._thread.name))
            raise "Unable to create a thread"

    def start(self):
        self._thread.start()
