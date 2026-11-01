from posture_engine import analyze_exercise_posture


# Create 33 simulated MediaPipe landmarks
landmarks = []

for i in range(33):
    landmarks.append({
        "x": 0.5,
        "y": 0.5,
        "visibility": 1.0
    })


# Simulate ear, shoulder and hip positions
landmarks[7]["x"] = 0.55
landmarks[7]["y"] = 0.30

landmarks[11]["x"] = 0.50
landmarks[11]["y"] = 0.40

landmarks[23]["x"] = 0.50
landmarks[23]["y"] = 0.70


# Analyze posture
result = analyze_exercise_posture(
    landmarks,
    "squat",
    640,
    480
)

print("Posture Analysis Result:")
print(result)