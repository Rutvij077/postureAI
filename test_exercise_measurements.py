from posture_engine import analyze_exercise_measurements


# Create 33 simulated landmarks
class Landmark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visibility = 1.0


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


result = analyze_exercise_measurements(
    landmarks,
    "bicep_curl",
    640,
    480
)

print(result)