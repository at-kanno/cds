import unittest

from sql import parse_question_row


class SqlImportTests(unittest.TestCase):
    def test_thirteen_columns(self) -> None:
        row = (
            201,
            21,
            1,
            "Q",
            "A1",
            "A2",
            "A3",
            "A4",
            1,
            2,
            3,
            4,
            0,
        )
        parsed = parse_question_row(row)
        self.assertEqual(parsed[0], 201)
        self.assertEqual(parsed[1], 21)
        self.assertEqual(parsed[12], 0)

    def test_fourteen_columns_memo_ignored(self) -> None:
        row = (
            201,
            21,
            1,
            "Q",
            "A1",
            "A2",
            "A3",
            "Prompt",
            1,
            2,
            3,
            None,
            101,
            "memo: set id note",
        )
        parsed = parse_question_row(row)
        assert parsed is not None
        self.assertEqual(len(parsed), 13)
        self.assertEqual(parsed[0], 201)
        self.assertEqual(parsed[7], "Prompt")
        self.assertIsNone(parsed[11])  # cid4 empty
        self.assertEqual(parsed[12], 101)

    def test_empty_integer_cells_become_none(self) -> None:
        row = (
            101.0,
            11,
            None,
            "Q",
            "A1",
            "A2",
            "A3",
            "A4",
            "",
            None,
            None,
            None,
            "",
        )
        parsed = parse_question_row(row)
        assert parsed is not None
        self.assertEqual(parsed[0], 101)
        self.assertIsNone(parsed[2])  # level
        self.assertIsNone(parsed[8])  # cid1
        self.assertIsNone(parsed[12])  # flag

    def test_blank_row_skipped(self) -> None:
        self.assertIsNone(parse_question_row((None,) * 14))
        self.assertIsNone(parse_question_row(()))


if __name__ == "__main__":
    unittest.main()
