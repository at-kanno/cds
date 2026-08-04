import unittest

from examDB import _safe_int


class SafeIntFlagTests(unittest.TestCase):
    def test_parses_integers(self) -> None:
        self.assertEqual(_safe_int(101), 101)
        self.assertEqual(_safe_int("215"), 215)

    def test_legacy_flag_strings_become_zero(self) -> None:
        self.assertEqual(_safe_int("2.2.f"), 0)
        self.assertEqual(_safe_int("1-12(2)"), 0)
        self.assertEqual(_safe_int(None), 0)
        self.assertEqual(_safe_int(""), 0)


if __name__ == "__main__":
    unittest.main()
