import os
import unittest
from unittest.mock import patch

from examDB import (
    allocate_set_counts,
    find_exam_q_no_for_number,
    get_passage_settings_for_category,
    order_passage_selection,
    resolve_passage_count,
)


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
        self.assertEqual(settings["flag_min"], 101)
        self.assertEqual(settings["flag_max"], 199)

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

    def test_toeic_part3_set_settings(self) -> None:
        os.environ["APP_PROFILE"] = "TOEIC"
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache

        clear_config_cache()
        clear_exam_plan_cache()
        settings = get_passage_settings_for_category(31)
        self.assertIsNotNone(settings)
        assert settings is not None
        self.assertEqual(settings["group"], "flag")
        self.assertEqual(settings["passages"], 2)
        self.assertEqual(settings["set_size"], 3)
        self.assertEqual(settings["flag_min"], 301)
        self.assertEqual(settings["flag_max"], 399)
        self.assertTrue(settings["order_by_number"])
        self.assertEqual(resolve_passage_count(5, settings), 2)
        self.assertEqual(resolve_passage_count(3, settings), 1)
        self.assertEqual(resolve_passage_count(2, settings), 1)

    def test_allocate_set_counts_five_is_three_plus_two(self) -> None:
        self.assertEqual(allocate_set_counts(5, 3, 2), [3, 2])
        self.assertEqual(allocate_set_counts(3, 3, 1), [3])
        self.assertEqual(allocate_set_counts(2, 3, 1), [2])
        self.assertEqual(allocate_set_counts(6, 3, 2), [3, 3])

    def test_toeic_five_questions_are_full_set_then_two_with_heads(self) -> None:
        groups = {
            301: [303, 301, 302],
            304: [306, 304, 305],
            307: [307, 308, 309],
        }

        def choose(candidates, *_args, **_kwargs):
            # First block (count=3) prefers 301; second (count=2) prefers 304.
            if 301 in candidates:
                return 301
            if 304 in candidates:
                return 304
            return candidates[0]

        with patch("examDB.random.choice", side_effect=choose):
            with patch("examDB.random.sample", side_effect=lambda seq, k: sorted(seq)[:k]):
                result = order_passage_selection(
                    groups,
                    passage_count=2,
                    amount=5,
                    flag_min=301,
                    flag_max=399,
                    set_size=3,
                )

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(len(result), 5)
        # 3 + 2 blocks; each block starts with its FLAG head.
        self.assertEqual(result[0], 301)
        self.assertEqual(result[:3], [301, 302, 303])
        self.assertEqual(result[3], 304)
        self.assertEqual(len(result[3:]), 2)
        self.assertTrue(all(n in {304, 305, 306} for n in result[3:]))
        self.assertIn(304, result[3:])

    def test_find_exam_q_no_for_number(self) -> None:
        examlist = "(101:1,2,3,4)(301:1,2,3,4)(302:2,1,3,4)"
        self.assertEqual(find_exam_q_no_for_number(examlist, 301), 2)
        self.assertEqual(find_exam_q_no_for_number(examlist, 302), 3)
        self.assertIsNone(find_exam_q_no_for_number(examlist, 999))


if __name__ == "__main__":
    unittest.main()
