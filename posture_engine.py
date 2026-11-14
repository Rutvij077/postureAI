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

def analyze_exercise_measurements(
    landmarks,
    exercise,
    image_width,
    image_height
):

    from exercise_rules import EXERCISES

    if exercise not in EXERCISES:
        raise ValueError(f"Unsupported exercise: {exercise}")

    config = EXERCISES[exercise]

    points = extract_landmarks(
        landmarks,
        image_width,
        image_height
    )

    measurements = {}
    missing_measurements = []
    unsupported_measurements = []

    # Head alignment
    if "head_alignment" in config["measurements"]:

        ear = points["left_ear"]
        shoulder = points["left_shoulder"]
        hip = points["left_hip"]

        if ear is not None and shoulder is not None and hip is not None:

            torso_length = np.linalg.norm(
                np.array(shoulder) - np.array(hip)
            )

            measurements["head_offset"] = calculate_head_offset(
                ear,
                shoulder,
                torso_length
            )

            if measurements["head_offset"] is None:
                missing_measurements.append("head_alignment")

        else:
            missing_measurements.append("head_alignment")

    # Torso inclination
    # Also calculate it internally when torso_stability is required.
    if (
        "torso_inclination" in config["measurements"]
        or "torso_stability" in config["measurements"]
    ):

        shoulder = points["left_shoulder"]
        hip = points["left_hip"]

        if shoulder is not None and hip is not None:

            measurements["torso_angle_degrees"] = (
                calculate_torso_inclination(shoulder, hip)
            )

            if measurements["torso_angle_degrees"] is None:
                if "torso_inclination" in config["measurements"]:
                    missing_measurements.append("torso_inclination")

                if "torso_stability" in config["measurements"]:
                    missing_measurements.append("torso_stability")

        else:
            if "torso_inclination" in config["measurements"]:
                missing_measurements.append("torso_inclination")

            if "torso_stability" in config["measurements"]:
                missing_measurements.append("torso_stability")

    # Elbow angle
    if "elbow_angle" in config["measurements"]:

        shoulder = points["left_shoulder"]
        elbow = points["left_elbow"]
        wrist = points["left_wrist"]

        if (
            shoulder is not None
            and elbow is not None
            and wrist is not None
        ):

            measurements["elbow_angle_degrees"] = (
                calculate_elbow_angle(
                    shoulder,
                    elbow,
                    wrist
                )
            )

        else:
            missing_measurements.append("elbow_angle")

    
    # Arm alignment
    if "arm_alignment" in config["measurements"]:

        left_shoulder = points["left_shoulder"]
        left_elbow = points["left_elbow"]

        right_shoulder = points["right_shoulder"]
        right_elbow = points["right_elbow"]

        if left_shoulder is not None and left_elbow is not None:

            measurements["left_arm_alignment_degrees"] = (
                calculate_arm_alignment(
                    left_shoulder,
                    left_elbow
                )
            )

        if right_shoulder is not None and right_elbow is not None:

            measurements["right_arm_alignment_degrees"] = (
                calculate_arm_alignment(
                    right_shoulder,
                    right_elbow
                )
            )

        if (
            "left_arm_alignment_degrees" not in measurements
            or "right_arm_alignment_degrees" not in measurements
        ):
            missing_measurements.append("arm_alignment")


    # Shoulder symmetry
    if "shoulder_symmetry" in config["measurements"]:

        left = points["left_shoulder"]
        right = points["right_shoulder"]

        if left is not None and right is not None:

            measurements["shoulder_asymmetry_pixels"] = (
                calculate_shoulder_asymmetry(left, right)
            )

        else:
            missing_measurements.append("shoulder_symmetry")

        # Body alignment
    if "body_alignment" in config["measurements"]:

        shoulder = points["left_shoulder"]
        hip = points["left_hip"]
        ankle = points["left_ankle"]

        if (
            shoulder is not None
            and hip is not None
            and ankle is not None
        ):

            measurements["body_alignment_degrees"] = (
                calculate_body_alignment(
                    shoulder,
                    hip,
                    ankle
                )
            )

        else:
            missing_measurements.append("body_alignment")

    # Hip alignment
    if "hip_alignment" in config["measurements"]:

        shoulder = points["left_shoulder"]
        hip = points["left_hip"]
        ankle = points["left_ankle"]

        if (
            shoulder is not None
            and hip is not None
            and ankle is not None
        ):

            measurements["hip_deviation_pixels"] = (
                calculate_hip_deviation(
                    shoulder,
                    hip,
                    ankle
                )
            )

        else:
            missing_measurements.append("hip_alignment")

        # Knee angle
    if "knee_angle" in config["measurements"]:

        hip = points["left_hip"]
        knee = points["left_knee"]
        ankle = points["left_ankle"]

        if (
            hip is not None
            and knee is not None
            and ankle is not None
        ):

            measurements["knee_angle_degrees"] = (
                calculate_knee_angle(
                    hip,
                    knee,
                    ankle
                )
            )

        else:
            missing_measurements.append("knee_angle")

        # Hip hinge
    if "hip_hinge" in config["measurements"]:

        shoulder = points["left_shoulder"]
        hip = points["left_hip"]
        knee = points["left_knee"]

        if (
            shoulder is not None
            and hip is not None
            and knee is not None
        ):

            measurements["hip_hinge_degrees"] = (
                calculate_hip_hinge(
                    shoulder,
                    hip,
                    knee
                )
            )

        else:
            missing_measurements.append("hip_hinge")

    # Hip depth
    if "hip_depth" in config["measurements"]:

        hip = points["left_hip"]
        knee = points["left_knee"]
        ankle = points["left_ankle"]

        if (
            hip is not None
            and knee is not None
            and ankle is not None
        ):

            measurements["hip_depth_ratio"] = (
                calculate_hip_depth(
                    hip,
                    knee,
                    ankle
                )
            )

        else:
            missing_measurements.append("hip_depth")

    
    # Front-view torso alignment
    if "torso_alignment" in config["measurements"]:

        left_shoulder = points["left_shoulder"]
        right_shoulder = points["right_shoulder"]

        left_hip = points["left_hip"]
        right_hip = points["right_hip"]

        alignment = calculate_torso_alignment(
            left_shoulder,
            right_shoulder,
            left_hip,
            right_hip
        )

        if alignment is not None:
            measurements["torso_alignment_degrees"] = alignment
        else:
            missing_measurements.append("torso_alignment")


    # Identify measurements not implemented yet
    implemented = {
        "head_alignment",
        "torso_inclination",
        "torso_stability",
        "elbow_angle",
        "shoulder_symmetry",
        "body_alignment",
        "hip_alignment",
        "knee_angle",
        "hip_depth",
        "hip_hinge",
        "arm_alignment",
        "torso_alignment"
    }

    for measurement in config["measurements"]:

        if measurement not in implemented:
            unsupported_measurements.append(measurement)

    # Determine analysis status
    if missing_measurements or unsupported_measurements:
        status = "partial"
    elif measurements:
        status = "measurements_available"
    else:
        status = "no_measurements_available"

    return {
        "exercise": exercise,
        "status": status,
        "measurements": measurements,
        "missing_measurements": missing_measurements,
        "unsupported_measurements": unsupported_measurements
    }

class ExerciseAnalyzer:


    def __init__(self, stability_window=30, smoothing_window=5):

        from measurement_smoothing import (
            TorsoStabilityTracker,
            MeasurementSmoother
        )

        self.stability_tracker = TorsoStabilityTracker(
            window_size=stability_window
        )

        self.smoother = MeasurementSmoother(
            window_size=smoothing_window
        )

        self.current_exercise = None

    def reset(self):

        self.stability_tracker.reset()
        self.smoother.reset()
        self.current_exercise = None

    def analyze_frame(
        self,
        landmarks,
        exercise,
        image_width,
        image_height
    ):

        # Reset history when the selected exercise changes
        if exercise != self.current_exercise:

            self.stability_tracker.reset()
            self.current_exercise = exercise

        result = analyze_exercise_measurements(
            landmarks,
            exercise,
            image_width,
            image_height
        )

        from exercise_rules import EXERCISES

        config = EXERCISES[exercise]

        if "torso_stability" in config["measurements"]:

            torso_angle = result["measurements"].get(
                "torso_angle_degrees"
            )

            if torso_angle is None:

                self.stability_tracker.reset()
                variation = None

            else:

                variation = self.stability_tracker.update(
                    torso_angle
                )

            result["measurements"]["torso_variation_degrees"] = variation

            # Stability needs at least two valid frames
            if variation is None:
                if "torso_stability" not in result["missing_measurements"]:
                    result["missing_measurements"].append(
                        "torso_stability"
                    )

            else:
                if "torso_stability" in result["missing_measurements"]:
                    result["missing_measurements"].remove(
                        "torso_stability"
                    )

        # Recalculate status after temporal analysis
        if (
            result["missing_measurements"]
            or result["unsupported_measurements"]
        ):
            result["status"] = "partial"

        elif result["measurements"]:
            result["status"] = "measurements_available"

        else:
            result["status"] = "no_measurements_available"

        return self.smoother.smooth(result)

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

def calculate_body_alignment(shoulder, hip, ankle):
    return calculate_angle(
        shoulder,
        hip,
        ankle
    )

def calculate_hip_deviation(shoulder, hip, ankle):

    start = np.array(shoulder, dtype=float)
    point = np.array(hip, dtype=float)
    end = np.array(ankle, dtype=float)

    line = end - start

    line_length = np.linalg.norm(line)

    if line_length < 1e-6:
        return None

    deviation = (
        line[0] * (point[1] - start[1])
        - line[1] * (point[0] - start[0])
    )

    return float(deviation / line_length)

def calculate_knee_angle(hip, knee, ankle):
    return calculate_angle(
        hip,
        knee,
        ankle
    )

def calculate_hip_depth(hip, knee, ankle):

    hip = np.array(hip, dtype=float)
    knee = np.array(knee, dtype=float)
    ankle = np.array(ankle, dtype=float)

    thigh_length = np.linalg.norm(hip - knee)

    if thigh_length < 1e-6:
        return None

    vertical_difference = hip[1] - knee[1]

    return float(vertical_difference / thigh_length)

def calculate_hip_hinge(shoulder, hip, knee):

    return calculate_angle(
        shoulder,
        hip,
        knee
    )


def calculate_arm_alignment(shoulder, elbow):

    if shoulder is None or elbow is None:
        return None

    shoulder = np.array(shoulder)
    elbow = np.array(elbow)

    arm_vector = elbow - shoulder

    # Compare the upper arm against the vertical axis
    horizontal_distance = abs(arm_vector[0])
    vertical_distance = abs(arm_vector[1])

    if np.linalg.norm(arm_vector) < 1e-6:
        return None

    angle = np.degrees(
        np.arctan2(horizontal_distance, vertical_distance)
    )

    return round(float(angle), 2)


def calculate_torso_alignment(
    left_shoulder,
    right_shoulder,
    left_hip,
    right_hip
):

    if any(
        point is None
        for point in [
            left_shoulder,
            right_shoulder,
            left_hip,
            right_hip
        ]
    ):
        return None

    # Calculate the midpoint between both shoulders
    shoulder_midpoint = (
        np.array(left_shoulder) + np.array(right_shoulder)
    ) / 2

    # Calculate the midpoint between both hips
    hip_midpoint = (
        np.array(left_hip) + np.array(right_hip)
    ) / 2

    # Calculate torso inclination using the centre line
    angle = calculate_torso_inclination(
        shoulder_midpoint,
        hip_midpoint
    )

    return round(float(angle), 2) if angle is not None else None

