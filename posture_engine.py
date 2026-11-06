import numpy as np
from feedback_rules import generate_feedback

LANDMARK_INDEX = {
    "nose": 0,
    "left_ear": 7,
    "right_ear": 8,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28
}

def extract_landmarks(landmarks, image_width, image_height):

    points = {}

    for name, index in LANDMARK_INDEX.items():

        landmark = landmarks[index]

        if landmark.visibility < 0.5:
            points[name] = None
            continue

        points[name] = (
            landmark.x * image_width,
            landmark.y * image_height
        )

    return points

def calculate_angle(a, b, c):
    """Calculate angle ABC in degrees."""

    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    ba = a - b
    bc = c - b

    denominator = (
        np.linalg.norm(ba) * np.linalg.norm(bc)
    )

    if denominator < 1e-8:
        return None

    cosine = np.dot(ba, bc) / denominator
    cosine = np.clip(cosine, -1.0, 1.0)

    return float(np.degrees(np.arccos(cosine)))

def analyze_posture(landmarks, exercise, image_width, image_height):
    from exercise_rules import EXERCISES

    if exercise not in EXERCISES:
        raise ValueError(f"Unsupported exercise: {exercise}")

    if isinstance(landmarks[7], dict):
        ear = type("Landmark", (), landmarks[7])()
        shoulder = type("Landmark", (), landmarks[11])()
        hip = type("Landmark", (), landmarks[23])()
    else:
        ear = landmarks[7]
        shoulder = landmarks[11]
        hip = landmarks[23]
        
    if min(
        ear.visibility,
        shoulder.visibility,
        hip.visibility
    ) < 0.5:
        return {
            "exercise": exercise,
            "status": "landmarks_unreliable",
            "message": "Adjust your position so your ear, shoulder and hip are visible."
        }

    ear_xy = (ear.x * image_width, ear.y * image_height)
    shoulder_xy = (
        shoulder.x * image_width,
        shoulder.y * image_height
    )
    hip_xy = (hip.x * image_width, hip.y * image_height)

    torso_length = np.linalg.norm(
        np.array(shoulder_xy) - np.array(hip_xy)
    )

    if torso_length < 1e-6:
        return {
            "exercise": exercise,
            "status": "invalid_measurement",
            "message": "Unable to estimate torso alignment."
        }

    head_offset = (
        ear_xy[0] - shoulder_xy[0]
    ) / torso_length

    vertical_reference = (
        hip_xy[0],
        hip_xy[1] - 100
    )

    torso_angle = calculate_angle(
        vertical_reference,
        hip_xy,
        shoulder_xy
    )

    return {
        "exercise": exercise,
        "status": "measurements_available",
        "head_offset": round(float(head_offset), 3),
        "torso_angle_degrees": (
            round(torso_angle, 1)
            if torso_angle is not None
            else None
        )
    }

def analyze_exercise_posture(
    landmarks,
    exercise,
    image_width,
    image_height
):
    measurements = analyze_posture(
        landmarks,
        exercise,
        image_width,
        image_height
    )

    feedback = generate_feedback(measurements)

    measurements["feedback"] = feedback

    return measurements

def calculate_elbow_angle(shoulder, elbow, wrist):
    return calculate_angle(
        shoulder,
        elbow,
        wrist
    )

def calculate_torso_inclination(shoulder, hip):
    vertical_reference = (
        hip[0],
        hip[1] - 100
    )

    return calculate_angle(
        vertical_reference,
        hip,
        shoulder
    )

def calculate_head_offset(ear, shoulder, torso_length):

    if torso_length < 1e-6:
        return None

    return (ear[0] - shoulder[0]) / torso_length

def calculate_shoulder_asymmetry(left_shoulder, right_shoulder):

    return abs(
        left_shoulder[1] - right_shoulder[1]
    )