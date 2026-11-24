"""Testet për demon e kontrollit të kllapave. Ekzekutimi: python -m unittest -v"""

import unittest

from demos.bracket_matching import check_brackets


class TestBracketMatching(unittest.TestCase):

    def test_balanced_cases(self):
        for text in ["", "abc", "()", "([]{})", "{[()()]}", "f(a[0], {b: c})"]:
            with self.subTest(text=text):
                self.assertTrue(check_brackets(text).balanced)

    def test_closing_without_opening(self):
        result = check_brackets("a)")
        self.assertFalse(result.balanced)
        self.assertEqual(result.position, 1)

    def test_mismatched_pair(self):
        result = check_brackets("(]")
        self.assertFalse(result.balanced)
        self.assertEqual(result.position, 1)

    def test_wrong_nesting_order(self):
        result = check_brackets("([)]")
        self.assertFalse(result.balanced)
        self.assertEqual(result.position, 2)

    def test_unclosed_opening(self):
        result = check_brackets("(()")
        self.assertFalse(result.balanced)
        self.assertEqual(result.position, 0)  # kllapa e parë mbetet e pambyllur

    def test_extra_closing_at_end(self):
        result = check_brackets("(a))")
        self.assertFalse(result.balanced)
        self.assertEqual(result.position, 3)


if __name__ == "__main__":
    unittest.main()
