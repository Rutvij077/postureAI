from collections import deque
import numpy as np


class MeasurementSmoother:

    def __init__(self, window_size=5):
        self.window_size = window_size

        self.head_offsets = deque(maxlen=window_size)
        self.torso_angles = deque(maxlen=window_size)

    def reset(self):
        self.head_offsets.clear()
        self.torso_angles.clear()

    def smooth(self, measurements):

        # Reset history if measurements are unreliable
        if measurements["status"] != "measurements_available":
            self.reset()
            return measurements

        self.head_offsets.append(measurements["head_offset"])

        if measurements["torso_angle_degrees"] is not None:
            self.torso_angles.append(
                measurements["torso_angle_degrees"]
            )

        smoothed_head = (
            sum(self.head_offsets) / len(self.head_offsets)
        )

        smoothed_torso = None

        if self.torso_angles:
            smoothed_torso = (
                sum(self.torso_angles) / len(self.torso_angles)
            )

        measurements["head_offset"] = round(smoothed_head, 3)

        measurements["torso_angle_degrees"] = (
            round(smoothed_torso, 1)
            if smoothed_torso is not None
            else None
        )

        return measurements

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