from posture_engine import (
    calculate_knee_angle,
    calculate_hip_depth
)

# Straight leg
hip = (100, 100)
knee = (100, 200)
ankle = (100, 300)

print(
    "Straight knee angle:",
    calculate_knee_angle(hip, knee, ankle)
)

print(
    "Hip depth:",
    calculate_hip_depth(hip, knee, ankle)
)


# Bent knee
hip = (100, 100)
knee = (100, 200)
ankle = (150, 250)

print(
    "Bent knee angle:",
    calculate_knee_angle(hip, knee, ankle)
)