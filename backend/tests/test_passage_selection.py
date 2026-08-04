import os
import unittest
from unittest.mock import patch

from examDB import get_passage_settings_for_category, order_passage_selection


class PassageSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.previous_profile = os.environ.get("APP_PROFILE")
        os.environ["APP_PROFILE"] = "SPANISH4"
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache

        clear_config_cache()
        clear_exam_plan_cache()

    def tearDown(self) -> None:
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache

        clear_config_cache()
        clear_exam_plan_cache()
        if self.previous_profile is None:
            os.environ.pop("APP_PROFILE", None)
        else:
            os.environ["APP_PROFILE"] = self.previous_profile

    def test_reading2_uses_flag_passages(self) -> None:
        settings = get_passage_settings_for_category(51)
        self.assertIsNotNone(settings)
        assert settings is not None
        self.assertEqual(settings["group"], "flag")
        self.assertEqual(settings["passages"], 2)

    def test_grammar_has_no_passage_settings(self) -> None:
        self.assertIsNone(get_passage_settings_for_category(11))

    def test_selects_two_passages_and_keeps_blocks(self) -> None:
        groups = {
            101: [1, 2, 3],
            102: [4, 5, 6],
            103: [7, 8, 9],
        }
        with patch("examDB.random.sample", side_effect=[[101, 102], [1, 2, 3, 4, 5]]):
            with patch("examDB.random.shuffle", side_effect=lambda xs: None):
                result = order_passage_selection(groups, passage_count=2, amount=5)

        self.assertEqual(result, [1, 2, 3, 4, 5])
        # First contiguous block is all from 101, remainder from 102
        self.assertEqual(result[:3], [1, 2, 3])
        self.assertTrue(all(n in {4, 5, 6} for n in result[3:]))

    def test_flag_with_five_members_all_eligible(self) -> None:
        groups = {
            110: [11, 12, 13, 14, 15],  # 5 items sharing one FLAG
            111: [21, 22, 23],
        }
        with patch("examDB.random.sample", side_effect=[[110, 111], [11, 12, 13, 14, 15]]):
            with patch("examDB.random.shuffle", side_effect=lambda xs: None):
                result = order_passage_selection(groups, passage_count=2, amount=5)

        self.assertEqual(sorted(result), [11, 12, 13, 14, 15])
        self.assertEqual(result, [11, 12, 13, 14, 15])

    def test_ignores_flag_outside_101_199(self) -> None:
        groups = {
            0: [1, 2, 3],
            100: [10, 11, 12],
            200: [20, 21, 22],
            101: [4, 5, 6],
            102: [7, 8, 9],
        }
        result = order_passage_selection(groups, passage_count=2, amount=5)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertTrue(all(n in {4, 5, 6, 7, 8, 9} for n in result))

    def test_fails_when_not_enough_passages(self) -> None:
        groups = {101: [1, 2, 3]}
        self.assertIsNone(order_passage_selection(groups, passage_count=2, amount=5))


if __name__ == "__main__":
    unittest.main()
