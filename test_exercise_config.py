
import unittest

from exercise_rules import EXERCISES, HOLD_TARGETS
from posture_engine import LANDMARK_INDEX


SUPPORTED_MEASUREMENTS = {
    "head_alignment",
    "torso_inclination",
    "hip_depth",
    "knee_angle",
    "hip_position",
    "hip_hinge",
    "torso_stability",
    "elbow_angle",
    "shoulder_symmetry",
    "torso_alignment",
    "body_alignment",
    "hip_alignment",
    "arm_alignment"
}


class TestExerciseConfig(unittest.TestCase):

    def test_required_fields_exist(self):
        required_fields = {
            "name",
            "view",
            "measurements",
            "landmarks"
        }

        for exercise, config in EXERCISES.items():
            with self.subTest(exercise=exercise):
                self.assertTrue(
                    required_fields.issubset(config.keys())
                )

    def test_valid_camera_views(self):
        for exercise, config in EXERCISES.items():
            with self.subTest(exercise=exercise):
                self.assertIn(config["view"], ["side", "front"])

    def test_supported_measurements(self):
        for exercise, config in EXERCISES.items():
            for measurement in config["measurements"]:
                with self.subTest(
                    exercise=exercise,
                    measurement=measurement
                ):
                    self.assertIn(
                        measurement,
                        SUPPORTED_MEASUREMENTS
                    )

    def test_valid_landmarks(self):

        valid_landmarks = {
            "nose",
            "ear",
            "shoulder",
            "hip",
            "knee",
            "ankle",
            "elbow",
            "wrist",
            "left_ear",
            "right_ear",
            "left_shoulder",
            "right_shoulder",
            "left_hip",
            "right_hip",
            "left_knee",
            "right_knee",
            "left_elbow",
            "right_elbow",
            "left_wrist",
            "right_wrist"
        }

        for exercise, config in EXERCISES.items():
            for landmark in config["landmarks"]:
                with self.subTest(
                    exercise=exercise,
                    landmark=landmark
                ):
                    self.assertIn(landmark, valid_landmarks)

    def test_hold_targets(self):
        for exercise, target in HOLD_TARGETS.items():
            with self.subTest(exercise=exercise):
                self.assertIn(exercise, EXERCISES)
                self.assertIsInstance(target, (int, float))
                self.assertGreater(target, 0)


if __name__ == "__main__":
    unittest.main()
