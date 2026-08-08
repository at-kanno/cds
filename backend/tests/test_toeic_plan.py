import os
import unittest
from collections import Counter
from unittest.mock import patch

from config_loader import clear_config_cache, get_exam_entry, get_menu_template
from exam_plan_loader import (
    clear_exam_plan_cache,
    resolve_assign_categories,
)
from menu_service import build_main_menu


class ToeicPlanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.previous = os.environ.get("APP_PROFILE")
        os.environ["APP_PROFILE"] = "TOEIC"
        clear_config_cache()
        clear_exam_plan_cache()

    def tearDown(self) -> None:
        clear_config_cache()
        clear_exam_plan_cache()
        if self.previous is None:
            os.environ.pop("APP_PROFILE", None)
        else:
            os.environ["APP_PROFILE"] = self.previous

    def test_part5_equal_from_fifteen(self) -> None:
        with patch("exam_plan_loader.random.shuffle", side_effect=lambda xs: None):
            cats = resolve_assign_categories(41)
        self.assertIsNotNone(cats)
        assert cats is not None
        self.assertEqual(len(cats), 50)
        part5 = [c for c in cats if 51 <= c <= 55]
        self.assertEqual(len(part5), 15)
        counts = Counter(part5)
        self.assertEqual(set(counts), {51, 52, 53, 54, 55})
        self.assertTrue(all(v == 3 for v in counts.values()))

    def test_listening_ten_distribution(self) -> None:
        cats = resolve_assign_categories(30)
        self.assertEqual(cats, [11, 11, 11, 21, 21, 21, 31, 31, 41, 41])

    def test_mock_exam_two_hundred(self) -> None:
        entry = get_exam_entry(70)
        assert entry is not None
        self.assertEqual(entry["amount"], 200)

    def test_hierarchical_menu_payload(self) -> None:
        menu = get_menu_template()
        self.assertTrue(menu["hierarchy"])
        top_actions = {item["action"] for item in menu["sections"][0]["items"]}
        self.assertEqual(top_actions, {"openSubmenu"})
        self.assertEqual(len(menu["submenus"]["single_question"]["items"]), 7)
        area_items = menu["submenus"]["area_quiz"]["items"]
        self.assertEqual(len(area_items), 11)
        area_cats = [item["category"] for item in area_items]
        self.assertEqual(area_cats, [10, 11, 12, 13, 141, 142, 143, 144, 145, 15, 16])
        self.assertEqual(len(menu["submenus"]["comprehensive"]["items"]), 8)

    def test_part5_category_field_quizzes(self) -> None:
        expected = {
            141: [51, 51, 51, 51, 51],
            142: [52, 52, 52, 52, 52],
            143: [53, 53, 53, 53, 53],
            144: [54, 54, 54, 54, 54],
            145: [55, 55, 55, 55, 55],
        }
        for exam_id, categories in expected.items():
            with self.subTest(exam_id=exam_id):
                entry = get_exam_entry(exam_id)
                self.assertIsNotNone(entry)
                assert entry is not None
                self.assertEqual(entry["amount"], 5)
                self.assertEqual(resolve_assign_categories(exam_id), categories)

    def test_build_main_menu_passes_submenus(self) -> None:
        with patch("menu_service.getStatus", return_value=0), patch(
            "menu_service.getLoginName", return_value="t@example.com"
        ):
            payload = build_main_menu(1)
        self.assertTrue(payload["hierarchy"])
        self.assertIn("comprehensive", payload["submenus"])
        self.assertEqual(payload["submenus"]["comprehensive"]["items"][-1]["category"], 70)


if __name__ == "__main__":
    unittest.main()
