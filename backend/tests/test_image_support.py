import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from image_support import get_image_info, is_safe_image_filename, resolve_image_path


class ImageSupportTests(unittest.TestCase):
    def test_safe_filename(self) -> None:
        self.assertTrue(is_safe_image_filename("101.png"))
        self.assertTrue(is_safe_image_filename("101.jpg"))
        self.assertFalse(is_safe_image_filename("../101.png"))
        self.assertFalse(is_safe_image_filename("abc.png"))

    def test_resolve_png_and_info(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = os.path.join(tmp, "TOEIC-1")
            os.makedirs(pack)
            path = os.path.join(pack, "101.png")
            with open(path, "wb") as handle:
                handle.write(b"\x89PNG")
            with patch.dict(os.environ, {"EXAM_IMAGE_DIR": tmp}):
                self.assertEqual(resolve_image_path(101), path)
                info = get_image_info(SimpleNamespace(number=101))
                self.assertIsNotNone(info)
                assert info is not None
                self.assertEqual(info["filename"], "101.png")

    def test_part3_set_image_uses_flag_for_all_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = os.path.join(tmp, "TOEIC-3")
            os.makedirs(pack)
            path = os.path.join(pack, "310.png")
            with open(path, "wb") as handle:
                handle.write(b"\x89PNG")
            with patch.dict(os.environ, {"EXAM_IMAGE_DIR": tmp}):
                self.assertEqual(resolve_image_path(311, 310), path)
                info = get_image_info(SimpleNamespace(number=312, flag=310))
                self.assertIsNotNone(info)
                assert info is not None
                self.assertEqual(info["filename"], "310.png")


if __name__ == "__main__":
    unittest.main()
