
from measurement_smoothing import MeasurementSmoother


smoother = MeasurementSmoother(window_size=3)

sample_values = [10, 20, 30, 40]

for value in sample_values:

    result = {
        "exercise": "bicep_curl",
        "status": "measurements_available",
        "measurements": {
            "torso_angle_degrees": value,
            "elbow_angle_degrees": 90
        },
        "missing_measurements": [],
        "unsupported_measurements": []
    }

    smoothed = smoother.smooth(result)

    print(
        "Raw torso angle:", value,
        "| Smoothed:", smoothed["measurements"]["torso_angle_degrees"]
    )
