from threading import Timer

from time import sleep


class TimerOnce(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



def hello(name):
    print "Hello %s!" % name


print "starting..."
rt = TimerOnce(1, hello, "World")  # it auto-starts, no need of rt.start()
try:
    sleep(5)  # your long-running job goes here...
finally:
    rt.stop()  # better in a try/finally block to make sure the program ends!