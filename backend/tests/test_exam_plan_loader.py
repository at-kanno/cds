import os
import unittest
from unittest.mock import patch

from config_loader import clear_config_cache, get_exam_entry, get_menu_template, get_areas
from exam_plan_loader import (
    clear_exam_plan_cache,
    count_exam_slots,
    get_exam_plan_entry,
    get_menu_from_plan,
    load_exam_plan,
    plan_exists,
    resolve_assign_categories,
)


class ExamPlanLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        clear_config_cache()
        clear_exam_plan_cache()
        self.previous_profile = os.environ.get("APP_PROFILE")
        os.environ["APP_PROFILE"] = "CDS"

    def tearDown(self) -> None:
        clear_config_cache()
        clear_exam_plan_cache()
        if self.previous_profile is None:
            os.environ.pop("APP_PROFILE", None)
        else:
            os.environ["APP_PROFILE"] = self.previous_profile

    def test_plan_exists_for_cds_and_spanish4(self) -> None:
        self.assertTrue(plan_exists("CDS"))
        self.assertTrue(plan_exists("SPANISH4"))

    def test_cds_category_10_slots(self) -> None:
        categories = resolve_assign_categories(10)
        self.assertEqual(categories, [11, 13, 11, 12, 11])

    def test_cds_category_30_pick_slot(self) -> None:
        with patch("exam_plan_loader.random.randint", return_value=1):
            categories = resolve_assign_categories(30)
        self.assertEqual(categories, [34, 31, 32, 33, 32])

        with patch("exam_plan_loader.random.randint", return_value=100):
            categories = resolve_assign_categories(30)
        self.assertEqual(categories[2], 34)

    def test_cds_full_exam_has_40_questions(self) -> None:
        categories = resolve_assign_categories(70)
        self.assertIsNotNone(categories)
        assert categories is not None
        self.assertEqual(len(categories), 40)
        self.assertEqual(categories[0], 31)

    def test_cds_category_60_uses_first_10(self) -> None:
        categories = resolve_assign_categories(60)
        full = resolve_assign_categories(70)
        assert categories is not None
        assert full is not None
        self.assertEqual(categories, full[:10])

    def test_menu_from_plan_cds(self) -> None:
        menu = get_menu_from_plan()
        self.assertIsNotNone(menu)
        assert menu is not None
        self.assertEqual(menu["title"], "メインメニュー")
        section_ids = [section["id"] for section in menu["sections"]]
        self.assertIn("final_exam", section_ids)

    def test_get_exam_entry_uses_yaml(self) -> None:
        entry = get_exam_entry(70)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["amount"], 40)
        self.assertEqual(entry["time_limit_seconds"], 5400)

    def test_spanish4_mock_exam_slots(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        clear_exam_plan_cache()
        categories = resolve_assign_categories(70)
        self.assertIsNotNone(categories)
        assert categories is not None
        self.assertEqual(len(categories), 35)
        self.assertTrue(
            set(categories[:10]).issubset({11, 12, 13, 16, 17, 18, 19})
        )
        self.assertEqual(categories[10:15], [21] * 5)

    def test_spanish4_grammar_split_from_pool(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        clear_exam_plan_cache()
        with patch("exam_plan_loader.random.choice", side_effect=[13, 17] * 3):
            categories = resolve_assign_categories(103)
        self.assertEqual(categories, [13, 17, 13, 17, 13])

        categories = resolve_assign_categories(101)
        self.assertEqual(categories, [11] * 5)

        with patch("exam_plan_loader.random.choice", side_effect=[18, 19, 18, 19, 18]):
            categories = resolve_assign_categories(104)
        self.assertEqual(categories, [18, 19, 18, 19, 18])

    def test_spanish4_menu_and_areas(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        clear_config_cache()
        clear_exam_plan_cache()
        menu = get_menu_template()
        self.assertEqual(menu["title"], "スペイン語検定4級 メニュー")
        areas = get_areas()
        self.assertEqual(len(areas), 6)
        entry = get_exam_plan_entry(101)
        assert entry is not None
        plan = load_exam_plan()
        assert plan is not None
        self.assertEqual(count_exam_slots(plan, plan["exams"]["101"]), 5)
        self.assertEqual(count_exam_slots(plan, plan["exams"]["105"]), 10)


if __name__ == "__main__":
    unittest.main()
