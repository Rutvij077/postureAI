from measurement_smoothing import MeasurementSmoother

smoother = MeasurementSmoother(window_size=3)

# Add three measurements
for value in [0.10, 0.20, 0.30]:

    result = {
        "status": "measurements_available",
        "head_offset": value,
        "torso_angle_degrees": 15.0
    }

    print(smoother.smooth(result)["head_offset"])


# Simulate tracking loss
lost_tracking = {
    "status": "landmarks_unreliable",
    "message": "Adjust your position."
}

print(smoother.smooth(lost_tracking))

# Add a fresh measurement
new_measurement = {
    "status": "measurements_available",
    "head_offset": 0.40,
    "torso_angle_degrees": 20.0
}

print(smoother.smooth(new_measurement)["head_offset"])