from measurement_smoothing import MeasurementSmoother

smoother = MeasurementSmoother(window_size=3)

for value in [0.10, 0.20, 0.30, 0.40]:

    result = {
        "status": "measurements_available",
        "head_offset": value,
        "torso_angle_degrees": 15.0
    }

    output = smoother.smooth(result)

    print(output["head_offset"])