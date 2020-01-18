from util.stopwatch import stopwatch as sw
import numpy as np

timer0=sw('bleh')
timer0.start()
kernel = np.ones((5, 5), np.uint8)
end= timer0.get()
print(end)