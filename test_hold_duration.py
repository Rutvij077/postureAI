
import time
from measurement_smoothing import HoldDurationTracker

tracker = HoldDurationTracker()

print(tracker.update(True))

time.sleep(1)

print(tracker.update(True))

print(tracker.update(False))

print(tracker.update(True))
