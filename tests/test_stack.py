"""Testet për klasën Stack. Ekzekutimi: python -m unittest -v"""

import unittest

from structures.stack import Stack, EmptyStackError


class TestStack(unittest.TestCase):

    def test_new_stack_is_empty(self):
        s = Stack()
        self.assertTrue(s.is_empty())
        self.assertEqual(len(s), 0)

    def test_push_then_peek(self):
        s = Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(len(s), 2)  # peek nuk e heq elementin

    def test_pop_is_lifo(self):
        s = Stack()
        for x in [1, 2, 3]:
            s.push(x)
        self.assertEqual([s.pop(), s.pop(), s.pop()], [3, 2, 1])
        self.assertTrue(s.is_empty())

    def test_pop_empty_raises(self):
        with self.assertRaises(EmptyStackError):
            Stack().pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(EmptyStackError):
            Stack().peek()

    def test_iter_goes_top_to_bottom(self):
        s = Stack(["a", "b", "c"])
        self.assertEqual(list(s), ["c", "b", "a"])
        self.assertEqual(len(s), 3)  # iterimi nuk e ndryshon Stack-un

    def test_push_after_emptying(self):
        s = Stack([1])
        s.pop()
        s.push(5)
        self.assertEqual(s.peek(), 5)
        self.assertEqual(len(s), 1)

    def test_repr(self):
        self.assertEqual(repr(Stack([1, 2])), "Stack(top -> [2, 1])")


if __name__ == "__main__":
    unittest.main()
