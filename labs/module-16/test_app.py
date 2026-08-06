import unittest

from app import summarize_scores


class SummarizeScoresTests(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(
            summarize_scores([]),
            {"count": 0, "average": None, "max": None},
        )

    def test_values(self):
        self.assertEqual(
            summarize_scores([10, 20, 25]),
            {"count": 3, "average": 18.33, "max": 25},
        )

    def test_mixed_numeric_types(self):
        self.assertEqual(
            summarize_scores([1, 2.5, 3]),
            {"count": 3, "average": 2.17, "max": 3},
        )

    def test_rejects_non_numeric(self):
        with self.assertRaises(TypeError):
            summarize_scores([1, "2", 3])


if __name__ == "__main__":
    unittest.main()
