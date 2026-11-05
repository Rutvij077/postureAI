from posture_engine import (
    calculate_angle,
    calculate_elbow_angle,
    calculate_torso_inclination,
    calculate_head_offset,
    calculate_shoulder_asymmetry
)

# Elbow angle
elbow_angle = calculate_elbow_angle(
    (0, 0),
    (1, 0),
    (1, 1)
)

print("Elbow angle:", elbow_angle)


# Torso inclination
torso_angle = calculate_torso_inclination(
    (100, 100),
    (100, 300)
)

print("Torso inclination:", torso_angle)


# Head offset
head_offset = calculate_head_offset(
    (120, 100),
    (100, 100),
    200
)

print("Head offset:", head_offset)


# Shoulder asymmetry
shoulder_difference = calculate_shoulder_asymmetry(
    (100, 100),
    (200, 110)
)

print("Shoulder asymmetry:", shoulder_difference)