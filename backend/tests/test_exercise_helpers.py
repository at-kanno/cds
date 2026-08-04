import os
import unittest

from exercise import _resolve_exam_lists


class ExerciseHelpersTests(unittest.TestCase):
    def test_resolve_exam_lists_keeps_existing_values(self) -> None:
        examlist, arealist = _resolve_exam_lists(
            "123", "(1:1,2,3,4)", "33333"
        )
        self.assertEqual(examlist, "(1:1,2,3,4)")
        self.assertEqual(arealist, "33333")

    def test_resolve_exam_lists_loads_from_db(self) -> None:
        os.environ["APP_PROFILE"] = "SPANISH4"
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache
        from examDB import makeExam2, saveExam, getExamlist

        clear_config_cache()
        clear_exam_plan_cache()

        result = makeExam2(1, 5, 40, 1, 600, "")
        self.assertIsNotNone(result)
        assert result is not None
        examlist, arealist = result
        exam_id = saveExam(1, "40", 1, 5, examlist, arealist)

        resolved_examlist, resolved_arealist = _resolve_exam_lists(
            str(exam_id), "", "33333"
        )
        self.assertEqual(resolved_examlist, examlist)
        self.assertEqual(resolved_arealist, "33333")

        db_examlist, db_arealist, _ = getExamlist(exam_id)
        resolved_examlist, resolved_arealist = _resolve_exam_lists(str(exam_id), "", "")
        self.assertEqual(resolved_examlist, db_examlist)
        self.assertEqual(resolved_arealist, db_arealist)


if __name__ == "__main__":
    unittest.main()
