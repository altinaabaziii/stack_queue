"""Testet për demon e planifikimit Round-Robin. Ekzekutimi: python -m unittest -v"""

import unittest

from demos.task_scheduler import round_robin


def order(finished):
    """Kthen çiftet (emri, koha e përfundimit) për krahasim të lehtë."""
    return [(t.name, t.finish_time) for t in finished]


class TestRoundRobin(unittest.TestCase):

    def test_example_order_and_times(self):
        # A5 B3 C1 D4, quantum 2:
        # A0-2 B2-4 C4-5(mbaroi) D5-7 A7-9 B9-10(mbaroi) D10-12(mbaroi) A12-13(mbaroi)
        result = round_robin([("A", 5), ("B", 3), ("C", 1), ("D", 4)], 2)
        self.assertEqual(order(result),
                         [("C", 5), ("B", 10), ("D", 12), ("A", 13)])

    def test_waiting_time(self):
        result = round_robin([("A", 5), ("B", 3), ("C", 1), ("D", 4)], 2)
        waits = {t.name: t.waiting_time for t in result}
        self.assertEqual(waits, {"A": 8, "B": 7, "C": 4, "D": 8})

    def test_large_quantum_is_fifo(self):
        # quantum më i madh se çdo detyrë -> asnjë s'kthehet, rendi mbetet FIFO
        result = round_robin([("X", 3), ("Y", 1), ("Z", 2)], 10)
        self.assertEqual(order(result), [("X", 3), ("Y", 4), ("Z", 6)])

    def test_single_task(self):
        self.assertEqual(order(round_robin([("A", 7)], 3)), [("A", 7)])

    def test_empty_task_list(self):
        self.assertEqual(round_robin([], 2), [])

    def test_total_time_is_sum_of_bursts(self):
        tasks = [("A", 4), ("B", 6), ("C", 3)]
        result = round_robin(tasks, 1)
        self.assertEqual(result[-1].finish_time, 4 + 6 + 3)

    def test_invalid_quantum_raises(self):
        for q in [0, -1]:
            with self.subTest(quantum=q):
                with self.assertRaises(ValueError):
                    round_robin([("A", 1)], q)

    def test_invalid_burst_raises(self):
        with self.assertRaises(ValueError):
            round_robin([("A", 0)], 2)


if __name__ == "__main__":
    unittest.main()
