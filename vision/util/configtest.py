from util.stopwatch import stopwatch
from util.config import run_config
import sys

sw=stopwatch('sw')
sw.start()
config = run_config(None)

if config:
    print('INFO: ' + str(config))
timer = sw.get()
print('INFO: stopwatch: %.3f' % timer)
