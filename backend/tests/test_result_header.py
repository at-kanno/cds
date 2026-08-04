import os
import unittest
from unittest.mock import patch


class GetResultHeaderTests(unittest.TestCase):
    def setUp(self) -> None:
        os.environ["APP_PROFILE"] = "CDS"
        from config_loader import clear_config_cache
        from exam_plan_loader import clear_exam_plan_cache
        import constant

        clear_config_cache()
        clear_exam_plan_cache()
        constant.readConstant()

    def test_get_result_reads_after_thirteen_prefix_columns(self) -> None:
        import constant
        from resultDB import getResult, _GET_RESULT_PREFIX

        self.assertEqual(_GET_RESULT_PREFIX, 13)
        self.assertEqual(constant.NumOfHeader, 6)  # profile value must not shift getResult

        num_cat = constant.NumOfCategory
        num_area = constant.NumOfArea
        # Build a fake SELECT row matching getResult's column order.
        prefix = [
            1,  # EXAM_ID
            9,  # USER_ID
            "模擬",  # EXAM_TYPE
            40,  # TOTAL
            28,  # TOTAL_R
            70.0,  # TOTAL_P
            50.0,  # HALF1
            60.0,  # HALF2
            40,  # RESPONSE
            70.0,  # CORRECT_RES_RATE
            100,  # REMAIN_TIME
            0.5,  # REMAIN_TIME_RATE
            66.0,  # LAST3
        ]
        self.assertEqual(len(prefix), 13)

        category_block = []
        for i in range(num_cat):
            category_block.extend([i + 1, i, float(i)])  # number, score, percent

        area_block = []
        for i in range(num_area):
            area_block.extend([10 + i, 7 + i, 70.0 + i])

        row = tuple(prefix + category_block + area_block + [1])

        with patch("resultDB.sqlite3.connect") as connect:
            cursor = connect.return_value.cursor.return_value
            cursor.fetchall.return_value = [row]
            cat_n, cat_s, cat_p, area_n, area_s, area_p = getResult(1)

        self.assertEqual(cat_n[0], 1)
        self.assertEqual(cat_s[0], 0)
        self.assertEqual(area_n[0], 10)
        self.assertEqual(area_s[0], 7)
        self.assertEqual(area_p[0], 70.0)


if __name__ == "__main__":
    unittest.main()
