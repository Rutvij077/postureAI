
import unittest

from exercise_rules import EXERCISES, EXERCISE_CATEGORIES


class TestExerciseCategories(unittest.TestCase):

    def test_only_two_categories_exist(self):
        self.assertEqual(
            set(EXERCISE_CATEGORIES.keys()),
            {"gym", "home"}
        )

    def test_all_category_exercises_exist(self):
        for category in EXERCISE_CATEGORIES.values():
            for exercise in category["exercises"]:
                self.assertIn(exercise, EXERCISES)

    def test_no_duplicate_exercise_assignments(self):
        assigned_exercises = []

        for category in EXERCISE_CATEGORIES.values():
            assigned_exercises.extend(category["exercises"])

        self.assertEqual(
            len(assigned_exercises),
            len(set(assigned_exercises))
        )

    def test_every_exercise_is_categorized(self):
        assigned_exercises = set()

        for category in EXERCISE_CATEGORIES.values():
            assigned_exercises.update(category["exercises"])

        self.assertEqual(
            assigned_exercises,
            set(EXERCISES.keys())
        )


if __name__ == "__main__":
    unittest.main()
