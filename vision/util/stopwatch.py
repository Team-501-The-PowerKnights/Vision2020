import time


class stopwatch:
    """ utility function which provides a stopwatch
        var = stopwatch('name')
        var.start()
        var.get()
    """

    def __init__(self, name):
        self.name = name
        self.start_time = 0
        self.get_time = 0
        self.elapsed = 0

    def start(self):
        self.start_time = time.time()
        self.elapsed = 0
        return self.elapsed

    def get(self):
        self.get_time = time.time()
        self.elapsed = self.get_time - self.start_time
        return self.elapsed


"""
from util.stopwatch import stopwatch (as stopwatch)
sw = stopwatch('test')
sw.start()

time.sleep(1)

sw2 = stopwatch('test2')
sw2.start()

time.sleep(4)

timer = sw.get()
timer2 = sw2.get()
print('timers: %.3f, %.3f' % (timer,timer2)) 

"""
