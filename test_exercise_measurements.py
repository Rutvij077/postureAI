from posture_engine import analyze_exercise_measurements


class Landmark:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visibility = 1.0


# Create 33 simulated landmarks
landmarks = [
    Landmark(0.5, 0.5)
    for _ in range(33)
]

# Simulate body positions
landmarks[7] = Landmark(0.52, 0.25)
landmarks[11] = Landmark(0.50, 0.40)
landmarks[13] = Landmark(0.60, 0.40)
landmarks[15] = Landmark(0.60, 0.55)
landmarks[23] = Landmark(0.50, 0.70)

# Analyze bicep curl
result = analyze_exercise_measurements(
    landmarks,
    "bicep_curl",
    640,
    480
)

print("Analysis result:")
print(result)

print("\nStatus:", result["status"])
print("Calculated:", result["measurements"])
print("Missing:", result["missing_measurements"])
print("Not implemented:", result["unsupported_measurements"])