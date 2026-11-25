
import unittest
from types import SimpleNamespace

from exercise_rules import EXERCISES
from posture_engine import (
    LANDMARK_INDEX,
    analyze_exercise_measurements
)


MEASUREMENT_OUTPUTS = {
    "head_alignment": ["head_offset"],
    "torso_inclination": ["torso_angle_degrees"],
    "torso_stability": ["torso_angle_degrees"],
    "elbow_angle": ["elbow_angle_degrees"],
    "arm_alignment": [
        "left_arm_alignment_degrees",
        "right_arm_alignment_degrees"
    ],
    "shoulder_symmetry": ["shoulder_asymmetry_pixels"],
    "body_alignment": ["body_alignment_degrees"],
    "hip_alignment": ["hip_deviation_pixels"],
    "knee_angle": ["knee_angle_degrees"],
    "hip_hinge": ["hip_hinge_degrees"],
    "hip_position": ["hip_position_ratio"],
    "hip_depth": ["hip_depth_ratio"],
    "torso_alignment": ["torso_alignment_degrees"]
}


def create_synthetic_landmarks():
    landmarks = []

    for index in range(33):
        x = 0.1 + (index % 5) * 0.12
        y = 0.1 + (index // 5) * 0.1

        landmarks.append(
            SimpleNamespace(
                x=x,
                y=y,
                visibility=1.0
            )
        )

    return landmarks


class TestMeasurementCoverage(unittest.TestCase):

    def test_all_exercises_produce_measurements(self):

        for exercise, config in EXERCISES.items():

            with self.subTest(exercise=exercise):

                landmarks = create_synthetic_landmarks()

                result = analyze_exercise_measurements(
                    landmarks,
                    exercise,
                    640,
                    480
                )

                self.assertEqual(
                    result["status"],
                    "measurements_available"
                )

                self.assertEqual(
                    result["missing_measurements"],
                    []
                )

                self.assertEqual(
                    result["unsupported_measurements"],
                    []
                )

                measurements = result["measurements"]

                for measurement in config["measurements"]:

                    output_keys = MEASUREMENT_OUTPUTS[measurement]

                    for key in output_keys:
                        self.assertIn(key, measurements)
                        self.assertIsNotNone(measurements[key])

    def test_missing_knee_landmark_is_reported(self):

        landmarks = create_synthetic_landmarks()

        landmarks[LANDMARK_INDEX["left_knee"]].visibility = 0.0

        result = analyze_exercise_measurements(
            landmarks,
            "squat",
            640,
            480
        )

        self.assertEqual(result["status"], "partial")

        self.assertIn(
            "knee_angle",
            result["missing_measurements"]
        )

        self.assertIn(
            "hip_depth",
            result["missing_measurements"]
        )

    def test_unsupported_exercise_raises_error(self):

        landmarks = create_synthetic_landmarks()

        with self.assertRaises(ValueError):
            analyze_exercise_measurements(
                landmarks,
                "invalid_exercise",
                640,
                480
            )


if __name__ == "__main__":
    unittest.main()
