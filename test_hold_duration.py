
import time
from measurement_smoothing import HoldDurationTracker

tracker = HoldDurationTracker(grace_period=0.3)

print("Start:", tracker.update(True))

time.sleep(0.5)

print("After 0.5 sec:", tracker.update(True))

# Brief detection failure
print("Temporary failure:", tracker.update(False))

time.sleep(0.2)

# Detection recovers within grace period
print("Recovered:", tracker.update(True))

# Long detection failure
time.sleep(0.4)

print("Long failure:", tracker.update(False))
