
import unittest
from unittest.mock import patch

from measurement_smoothing import HoldDurationTracker


class TestHoldDurationTracker(unittest.TestCase):

    def setUp(self):
        self.mock_time = patch(
            "measurement_smoothing.time.monotonic"
        ).start()

        self.mock_time.return_value = 0
        self.tracker = HoldDurationTracker(grace_period=0.3)

    def tearDown(self):
        patch.stopall()

    def test_timer_starts(self):
        duration = self.tracker.update(True)

        self.assertEqual(duration, 0)
        self.assertEqual(self.tracker.status, "VALID")

    def test_brief_detection_loss(self):
        self.tracker.update(True)

        self.mock_time.return_value = 0.2
        duration = self.tracker.update(False)

        self.assertEqual(self.tracker.status, "TEMPORARY LOSS")
        self.assertGreater(duration, 0)

    def test_timer_resets_after_grace_period(self):
        self.tracker.update(True)

        self.mock_time.return_value = 0.4
        self.tracker.update(False)

        self.mock_time.return_value = 0.51
        duration = self.tracker.update(False)

        self.assertEqual(duration, 0)
        self.assertEqual(self.tracker.status, "INVALID")

    def test_timer_continues_after_brief_loss(self):
        self.tracker.update(True)

        self.mock_time.return_value = 0.2
        self.tracker.update(False)

        self.mock_time.return_value = 0.25
        duration = self.tracker.update(True)

        self.assertEqual(self.tracker.status, "VALID")
        self.assertGreater(duration, 0)


if __name__ == "__main__":
    unittest.main()
