import os
import unittest
from unittest.mock import patch

from examDB import GetRandom, get_choice_count_for_category


class ChoiceCountTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache

        clear_config_cache()
        clear_exam_plan_cache()

    def test_get_random_three_choice_pads_with_zero(self) -> None:
        with patch("examDB.random.shuffle", side_effect=lambda xs: xs.reverse()):
            perm = GetRandom(3)
        self.assertEqual(len(perm), 4)
        self.assertEqual(perm[3], 0)
        self.assertEqual(sorted(perm[:3]), [1, 2, 3])

    def test_get_random_two_choice(self) -> None:
        perm = GetRandom(2)
        self.assertEqual(len(perm), 4)
        self.assertEqual(perm[2], 0)
        self.assertEqual(perm[3], 0)
        self.assertEqual(set(perm[:2]), {1, 2})

    def test_spanish4_area_choice_counts(self) -> None:
        self.assertEqual(get_choice_count_for_category(11), 4)
        self.assertEqual(get_choice_count_for_category(31), 3)
        self.assertEqual(get_choice_count_for_category(41), 3)
        self.assertEqual(get_choice_count_for_category(51), 2)
        self.assertEqual(get_choice_count_for_category(61), 3)


if __name__ == "__main__":
    unittest.main()
