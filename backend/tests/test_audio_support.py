import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from audio_support import (
    audio_filename_for_question,
    get_audio_play_info,
    get_listening_settings_for_category,
    is_listening_share_flag,
    is_safe_audio_filename,
    resolve_audio_path,
    resolve_audio_stem,
)


class AudioSupportTests(unittest.TestCase):
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

    def test_stem_uses_number_by_default(self) -> None:
        self.assertEqual(resolve_audio_stem(6101, 0), "6101")
        self.assertEqual(audio_filename_for_question(6101, 0), "6101.mp3")

    def test_stem_uses_shared_flag_201_299(self) -> None:
        self.assertTrue(is_listening_share_flag(201))
        self.assertTrue(is_listening_share_flag(299))
        self.assertFalse(is_listening_share_flag(200))
        self.assertFalse(is_listening_share_flag(101))
        self.assertEqual(resolve_audio_stem(6101, 215), "215")
        self.assertEqual(audio_filename_for_question(6101, 215), "215.mp3")

    def test_listening_settings_for_category_61(self) -> None:
        settings = get_listening_settings_for_category(61)
        self.assertIsNotNone(settings)
        assert settings is not None
        self.assertEqual(settings["max_audio_plays"], 2)
        self.assertIsNone(get_listening_settings_for_category(51))

    def test_safe_filename(self) -> None:
        self.assertTrue(is_safe_audio_filename("6101.mp3"))
        self.assertFalse(is_safe_audio_filename("../6101.mp3"))
        self.assertFalse(is_safe_audio_filename("6101.wav"))
        self.assertFalse(is_safe_audio_filename("abc.mp3"))

    def test_resolve_path_and_play_info(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "6101.mp3")
            with open(path, "wb") as handle:
                handle.write(b"ID3")
            with patch.dict(os.environ, {"EXAM_AUDIO_DIR": tmp}):
                self.assertEqual(resolve_audio_path(6101, 0), path)
                question = SimpleNamespace(number=6101, flag=0, category=61)
                info = get_audio_play_info(question)
                self.assertIsNotNone(info)
                assert info is not None
                self.assertEqual(info["filename"], "6101.mp3")
                self.assertEqual(info["max_audio_plays"], 2)

    def test_shared_flag_falls_back_to_number(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "6101.mp3")
            with open(path, "wb") as handle:
                handle.write(b"ID3")
            with patch.dict(os.environ, {"EXAM_AUDIO_DIR": tmp}):
                self.assertEqual(resolve_audio_path(6101, 215), path)


if __name__ == "__main__":
    unittest.main()
