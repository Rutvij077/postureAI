
from feedback_rules import generate_feedback


test_cases = [

    {
        "exercise": "bicep_curl",
        "status": "measurements_available",
        "measurements": {
            "head_offset": 0.10,
            "elbow_angle_degrees": 85.0,
            "torso_angle_degrees": 5.0,
            "torso_variation_degrees": 6.2
        },
        "missing_measurements": [],
        "unsupported_measurements": []
    },

    {
        "exercise": "squat",
        "status": "measurements_available",
        "measurements": {
            "head_offset": 0.08,
            "torso_angle_degrees": 25.0,
            "knee_angle_degrees": 95.0,
            "hip_depth_ratio": 0.8
        },
        "missing_measurements": [],
        "unsupported_measurements": []
    },

    {
        "exercise": "plank",
        "status": "measurements_available",
        "measurements": {
            "head_offset": 0.12,
            "body_alignment_degrees": 175.0,
            "hip_deviation_pixels": 12.0
        },
        "missing_measurements": [],
        "unsupported_measurements": []
    }

]


for result in test_cases:

    print("\n----------------------------")

    feedback = generate_feedback(result)

    for message in feedback:
        print("-", message)
