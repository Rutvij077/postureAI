from exercise_rules import EXERCISES
from posture_engine import calculate_angle

print("Supported exercises:")

for exercise, config in EXERCISES.items():
    print(f"{exercise}: {config['name']}")

print("Test angle:", calculate_angle((0, 1), (0, 0), (1, 0)))
print("All basic checks completed.")