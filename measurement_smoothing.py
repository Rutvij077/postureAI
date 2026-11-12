
from collections import deque
import numpy as np


class MeasurementSmoother:

    def __init__(self, window_size=5):

        self.window_size = window_size

        # Each measurement gets its own rolling history
        self.history = {}

    def reset(self):
        self.history.clear()

    def smooth(self, result):

        smoothed_result = result.copy()
        measurements = result.get("measurements", {}).copy()

        for key, value in measurements.items():

            # Smooth only numeric measurements
            if isinstance(value, (int, float)) and not isinstance(value, bool):

                if key not in self.history:
                    self.history[key] = deque(
                        maxlen=self.window_size
                    )

                self.history[key].append(value)

                measurements[key] = round(
                    sum(self.history[key]) / len(self.history[key]),
                    3
                )

            else:
                # Clear history when a measurement becomes unavailable
                if key in self.history:
                    self.history[key].clear()

        smoothed_result["measurements"] = measurements

        return smoothed_result


class TorsoStabilityTracker:

    def __init__(self, window_size=30):
        self.torso_angles = deque(maxlen=window_size)

    def update(self, torso_angle):

        if torso_angle is None:
            return None

        self.torso_angles.append(torso_angle)

        # Need at least two measurements
        if len(self.torso_angles) < 2:
            return None

        variation = np.std(self.torso_angles)

        return round(float(variation), 2)

    def reset(self):
        self.torso_angles.clear()
