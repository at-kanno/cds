import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from audio_support import (
    audio_filename_for_question,
    get_audio_play_info,
    get_choice_audio_info,
    get_listening_settings_for_category,
    is_listening_share_flag,
    is_safe_audio_filename,
    map_choice_audio_to_display,
    resolve_audio_path,
    resolve_audio_stem,
    resolve_choice_audio_paths,
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
        self.assertTrue(is_safe_audio_filename("101-A.mp3"))
        self.assertTrue(is_safe_audio_filename("201-Q.mp3"))
        self.assertFalse(is_safe_audio_filename("../6101.mp3"))
        self.assertFalse(is_safe_audio_filename("6101.wav"))
        self.assertFalse(is_safe_audio_filename("abc.mp3"))
        self.assertFalse(is_safe_audio_filename("101-E.mp3"))

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

    def test_resolve_mp3_from_image_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "101.mp3")
            with open(path, "wb") as handle:
                handle.write(b"ID3")
            with patch.dict(os.environ, {"EXAM_AUDIO_DIR": os.path.join(tmp, "missing"), "EXAM_IMAGE_DIR": tmp}):
                self.assertEqual(resolve_audio_path(101, 0), path)

    def test_choice_audio_from_image_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = os.path.join(tmp, "TOEIC-1")
            os.makedirs(pack)
            for letter in "ABCD":
                with open(os.path.join(pack, f"101-{letter}.mp3"), "wb") as handle:
                    handle.write(b"ID3")
            with patch.dict(
                os.environ,
                {"EXAM_AUDIO_DIR": os.path.join(tmp, "missing"), "EXAM_IMAGE_DIR": tmp, "APP_PROFILE": "TOEIC"},
            ):
                from config_loader import clear_config_cache
                from exam_plan_loader import clear_exam_plan_cache

                clear_config_cache()
                clear_exam_plan_cache()
                paths = resolve_choice_audio_paths(101)
                self.assertEqual(set(paths), {"A", "B", "C", "D"})
                question = SimpleNamespace(
                    number=101, flag=0, category=11, permutation=[1, 2, 3, 4]
                )
                info = get_choice_audio_info(question)
                self.assertIsNotNone(info)
                assert info is not None
                self.assertEqual(info["choices"]["A"], "101-A.mp3")
                self.assertIsNone(get_audio_play_info(question))

                remapped = SimpleNamespace(
                    number=101, flag=0, category=11, permutation=[2, 1, 3, 4]
                )
                info2 = get_choice_audio_info(remapped)
                assert info2 is not None
                self.assertEqual(info2["choices"]["A"], "101-B.mp3")
                self.assertEqual(info2["choices"]["B"], "101-A.mp3")
                self.assertEqual(info2["choices"]["C"], "101-C.mp3")
                self.assertEqual(info2["choices"]["D"], "101-D.mp3")

    def test_part2_question_and_choice_audio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = os.path.join(tmp, "TOEIC-2")
            os.makedirs(pack)
            for name in ("201-Q.mp3", "201-A.mp3", "201-B.mp3", "201-C.mp3"):
                with open(os.path.join(pack, name), "wb") as handle:
                    handle.write(b"ID3")
            with patch.dict(
                os.environ,
                {"EXAM_AUDIO_DIR": os.path.join(tmp, "missing"), "EXAM_IMAGE_DIR": tmp, "APP_PROFILE": "TOEIC"},
            ):
                from config_loader import clear_config_cache
                from exam_plan_loader import clear_exam_plan_cache

                clear_config_cache()
                clear_exam_plan_cache()
                question = SimpleNamespace(
                    number=201, flag=0, category=21, permutation=[2, 1, 3, 0]
                )
                stem = get_audio_play_info(question)
                choices = get_choice_audio_info(question)
                self.assertIsNotNone(stem)
                self.assertIsNotNone(choices)
                assert stem is not None and choices is not None
                self.assertEqual(stem["filename"], "201-Q.mp3")
                self.assertEqual(choices["choices"]["A"], "201-B.mp3")
                self.assertEqual(choices["choices"]["B"], "201-A.mp3")
                self.assertEqual(choices["choices"]["C"], "201-C.mp3")
                self.assertNotIn("D", choices["choices"])

    def test_map_choice_audio_to_display(self) -> None:
        paths = {
            "A": r"C:\tmp\101-A.mp3",
            "B": r"C:\tmp\101-B.mp3",
            "C": r"C:\tmp\101-C.mp3",
            "D": r"C:\tmp\101-D.mp3",
        }
        mapped = map_choice_audio_to_display(paths, "3142")
        self.assertEqual(mapped["A"], "101-C.mp3")
        self.assertEqual(mapped["B"], "101-A.mp3")
        self.assertEqual(mapped["C"], "101-D.mp3")
        self.assertEqual(mapped["D"], "101-B.mp3")


if __name__ == "__main__":
    unittest.main()
