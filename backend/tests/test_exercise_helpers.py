import unittest
from unittest.mock import patch

from exercise import _resolve_exam_lists


class ExerciseHelpersTests(unittest.TestCase):
    def test_resolve_exam_lists_keeps_existing_values(self) -> None:
        examlist, arealist = _resolve_exam_lists(
            "123", "(1:1,2,3,4)", "33333"
        )
        self.assertEqual(examlist, "(1:1,2,3,4)")
        self.assertEqual(arealist, "33333")

    def test_resolve_exam_lists_loads_from_db(self) -> None:
        with patch(
            "examDB.getExamlist",
            return_value=("(9:1,2,3,4)", "AAAAA", "00000"),
        ):
            resolved_examlist, resolved_arealist = _resolve_exam_lists(
                "42", "", "33333"
            )
        self.assertEqual(resolved_examlist, "(9:1,2,3,4)")
        self.assertEqual(resolved_arealist, "33333")

        with patch(
            "examDB.getExamlist",
            return_value=("(9:1,2,3,4)", "BBBBB", "00000"),
        ):
            resolved_examlist, resolved_arealist = _resolve_exam_lists("42", "", "")
        self.assertEqual(resolved_examlist, "(9:1,2,3,4)")
        self.assertEqual(resolved_arealist, "BBBBB")


if __name__ == "__main__":
    unittest.main()
