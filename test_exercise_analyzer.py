from types import SimpleNamespace

from posture_engine import ExerciseAnalyzer


def create_landmarks(shoulder_x):

    landmarks = [
        SimpleNamespace(x=0, y=0, visibility=0)
        for _ in range(33)
    ]

    # Required landmarks for bicep curl
    landmarks[7] = SimpleNamespace(
        x=shoulder_x, y=0.25, visibility=1
    )

    landmarks[11] = SimpleNamespace(
        x=shoulder_x, y=0.30, visibility=1
    )

    landmarks[23] = SimpleNamespace(
        x=0.50, y=0.60, visibility=1
    )

    landmarks[13] = SimpleNamespace(
        x=shoulder_x + 0.05, y=0.42, visibility=1
    )

    landmarks[15] = SimpleNamespace(
        x=shoulder_x + 0.10, y=0.35, visibility=1
    )

    return landmarks


analyzer = ExerciseAnalyzer(stability_window=5)

# Feed multiple frames with slightly changing torso angles
for x in [0.40, 0.42, 0.45, 0.48]:

    result = analyzer.analyze_frame(
        landmarks=create_landmarks(x),
        exercise="bicep_curl",
        image_width=640,
        image_height=480
    )

    print(result)

    print(
        "Torso variation:",
        result["measurements"].get("torso_variation_degrees")
    )

    print("-" * 40)