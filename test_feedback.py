
from feedback_rules import generate_feedback


sample_result = {
    "exercise": "bicep_curl",
    "status": "measurements_available",

    "measurements": {
        "head_offset": 0.12,
        "torso_angle_degrees": 8.5,
        "torso_variation_degrees": 2.3,
        "elbow_angle_degrees": 85.4
    },

    "missing_measurements": [],
    "unsupported_measurements": []
}


feedback = generate_feedback(sample_result)

for message in feedback:
    print("-", message)
