import os
import unittest
from unittest.mock import patch

from config_loader import (
    build_area_globals,
    clear_config_cache,
    get_exam_entry,
    get_menu_template,
    get_profile_name,
    get_profile_section,
)


class ConfigLoaderTests(unittest.TestCase):
    def setUp(self) -> None:
        clear_config_cache()
        self.previous_profile = os.environ.get("APP_PROFILE")
        os.environ["APP_PROFILE"] = "CDS"

    def tearDown(self) -> None:
        clear_config_cache()
        if self.previous_profile is None:
            os.environ.pop("APP_PROFILE", None)
        else:
            os.environ["APP_PROFILE"] = self.previous_profile

    def test_default_profile_is_cds(self) -> None:
        os.environ.pop("APP_PROFILE", None)
        clear_config_cache()
        self.assertEqual(get_profile_name(), "CDS")

    def test_cds_profile_has_menu(self) -> None:
        menu = get_menu_template()
        self.assertEqual(menu["title"], "メインメニュー")
        section_ids = [section["id"] for section in menu["sections"]]
        self.assertIn("single_question", section_ids)
        self.assertIn("mock_exam", section_ids)

    def test_cds_exam_catalog_multi_entry(self) -> None:
        entry = get_exam_entry(70)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["mode"], "multi")
        self.assertEqual(entry["amount"], 40)
        self.assertEqual(entry["time_limit_seconds"], 5400)

    def test_cds_exam_catalog_single_entry(self) -> None:
        entry = get_exam_entry(91)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["mode"], "single")
        self.assertEqual(entry["category_range"], [11, 19])

    def test_build_area_globals(self) -> None:
        areas = get_profile_section()["areas"]
        abbrev, areaname, practice, practice2, category_number = build_area_globals(areas)
        self.assertEqual(abbrev[0], "組織")
        self.assertEqual(category_number[:3], [11, 12, 13])
        self.assertEqual(len(practice2), 10)

    def test_toeic_profile(self) -> None:
        os.environ["APP_PROFILE"] = "TOEIC"
        clear_config_cache()
        menu = get_menu_template()
        self.assertEqual(menu["title"], "TOEIC メニュー")
        entry = get_exam_entry(70)
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["amount"], 200)

    def test_spanish4_profile(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        clear_config_cache()
        menu = get_menu_template()
        self.assertEqual(menu["title"], "スペイン語検定4級 メニュー")
        section_ids = [section["id"] for section in menu["sections"]]
        self.assertEqual(
            section_ids,
            ["single_question", "area_quiz", "mock_exam"],
        )
        mock = get_exam_entry(70)
        self.assertIsNotNone(mock)
        assert mock is not None
        self.assertEqual(mock["amount"], 35)
        self.assertEqual(mock["time_limit_seconds"], 3600)
        self.assertEqual(len(mock["assign_categories"]), 35)
        single = get_exam_entry(91)
        self.assertIsNotNone(single)
        assert single is not None
        self.assertEqual(single["time_limit_seconds"], 60)
        areas = get_profile_section()["areas"]
        self.assertEqual(len(areas), 6)
        _, _, _, _, category_number = build_area_globals(areas)
        self.assertEqual(category_number, [11, 21, 31, 41, 51, 61])


class MenuServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        clear_config_cache()
        self.previous_profile = os.environ.get("APP_PROFILE")
        os.environ["APP_PROFILE"] = "CDS"

    def tearDown(self) -> None:
        clear_config_cache()
        if self.previous_profile is None:
            os.environ.pop("APP_PROFILE", None)
        else:
            os.environ["APP_PROFILE"] = self.previous_profile

    def test_build_main_menu_locked_mock_exam(self) -> None:
        from menu_service import build_main_menu

        with patch("menu_service.getStatus", return_value=0), patch(
            "menu_service.getLoginName", return_value="test@example.com"
        ):
            menu = build_main_menu(user_id=1)
        mock_section = next(section for section in menu["sections"] if section["id"] == "mock_exam")
        self.assertFalse(mock_section["items"][0]["enabled"])

    def test_build_main_menu_structure(self) -> None:
        from menu_service import build_main_menu

        with patch("menu_service.getStatus", return_value=0), patch(
            "menu_service.getLoginName", return_value="test@example.com"
        ):
            menu = build_main_menu(user_id=1)
        self.assertEqual(menu["title"], "メインメニュー")
        self.assertTrue(menu["actions"])


if __name__ == "__main__":
    unittest.main()
