"""Testet për klasën Queue. Ekzekutimi: python -m unittest -v"""

import unittest

from structures.queue import Queue, EmptyQueueError


class TestQueue(unittest.TestCase):

    def test_new_queue_is_empty(self):
        q = Queue()
        self.assertTrue(q.is_empty())
        self.assertEqual(len(q), 0)

    def test_push_then_peek(self):
        q = Queue()
        q.push(1)
        q.push(2)
        self.assertEqual(q.peek(), 1)  # i pari që hyri
        self.assertEqual(len(q), 2)    # peek nuk e heq elementin

    def test_pop_is_fifo(self):
        q = Queue()
        for x in [1, 2, 3]:
            q.push(x)
        self.assertEqual([q.pop(), q.pop(), q.pop()], [1, 2, 3])
        self.assertTrue(q.is_empty())

    def test_pop_empty_raises(self):
        with self.assertRaises(EmptyQueueError):
            Queue().pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(EmptyQueueError):
            Queue().peek()

    def test_iter_goes_head_to_tail(self):
        q = Queue(["a", "b", "c"])
        self.assertEqual(list(q), ["a", "b", "c"])
        self.assertEqual(len(q), 3)  # iterimi nuk e ndryshon radhën

    def test_tail_reset_when_emptied(self):
        q = Queue([1])
        q.pop()
        self.assertIsNone(q._head)
        self.assertIsNone(q._tail)  # përndryshe _tail do të tregonte te nyja e hequr

    def test_push_after_emptying(self):
        q = Queue([1, 2])
        q.pop()
        q.pop()
        q.push(5)
        q.push(6)
        self.assertEqual(list(q), [5, 6])
        self.assertEqual(q.pop(), 5)
        self.assertEqual(len(q), 1)

    def test_interleaved_push_pop(self):
        q = Queue()
        q.push(1)
        q.push(2)
        self.assertEqual(q.pop(), 1)
        q.push(3)
        self.assertEqual(list(q), [2, 3])

    def test_enqueue_dequeue_aliases(self):
        q = Queue()
        q.enqueue("x")
        q.enqueue("y")
        self.assertEqual(q.dequeue(), "x")
        self.assertEqual(q.peek(), "y")

    def test_repr(self):
        self.assertEqual(repr(Queue([1, 2])), "Queue(head -> [1, 2] <- tail)")
        self.assertEqual(repr(Queue()), "Queue(head -> [] <- tail)")


if __name__ == "__main__":
    unittest.main()
