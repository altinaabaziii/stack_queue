"""Queue (Radha): strukturë FIFO (First In, First Out).

Përgjegjëse: Blenda Abazi

Implementimi përdor listë të lidhur me dy tregues: _head (fillimi, nga ku
dalin elementet) dhe _tail (fundi, ku hyjnë elementet):

   _head                       _tail
     |                           |
     v                           v
   [ A ] -> [ B ] -> [ C ] -> [ D ] -> None
   (del i pari)            (hyri i fundit)

    push  (enqueue) -> shton nyje të re pas _tail           O(1)
    pop   (dequeue) -> heq nyjen te _head                   O(1)
    peek            -> lexon vlerën te _head pa e hequr     O(1)

Pa treguesin _tail, shtimi në fund do të kërkonte kalimin nëpër gjithë
listën (O(n)). Me dy tregues, të dyja skajet arrihen menjëherë.
"""

from structures.node import Node


class EmptyQueueError(Exception):
    """Ngritet kur kërkohet pop ose peek nga një radhë e zbrazët."""


class Queue:
    """Radhë e implementuar me listë të lidhur, pa koleksione të gatshme."""

    def __init__(self, items=None):
        self._head = None   # nyja e parë (del e para)
        self._tail = None   # nyja e fundit (hyri e fundit)
        self._size = 0      # numri i elementeve
        if items is not None:
            for item in items:
                self.push(item)

    def push(self, value):
        """Shton `value` në fund të radhës. O(1)"""
        node = Node(value)
        if self._tail is None:
            # radha ishte bosh: nyja e re është njëkohësisht e para dhe e fundit
            self._head = node
        else:
            # nyja e fundit e vjetër tani tregon te nyja e re
            self._tail.next = node
        self._tail = node
        self._size += 1

    def pop(self):
        """Heq dhe kthen elementin në fillim të radhës. O(1)

        Ngre EmptyQueueError nëse radha është e zbrazët.
        """
        if self.is_empty():
            raise EmptyQueueError("pop nga radhë e zbrazët")
        node = self._head
        self._head = node.next
        if self._head is None:
            # radha u zbraz: edhe _tail duhet të mos tregojë më te nyja e hequr
            self._tail = None
        self._size -= 1
        return node.value

    def peek(self):
        """Kthen elementin në fillim pa e hequr. O(1)

        Ngre EmptyQueueError nëse radha është e zbrazët.
        """
        if self.is_empty():
            raise EmptyQueueError("peek në radhë të zbrazët")
        return self._head.value

    def is_empty(self):
        """Kthen True nëse radha nuk ka elemente. O(1)"""
        return self._head is None

    # Emrat klasikë të veprimeve të radhës (sinonime të push/pop)
    enqueue = push
    dequeue = pop

    def __len__(self):
        return self._size

    def __iter__(self):
        """Iteron nga fillimi drejt fundit, në rendin që do të dilnin me pop.

        Përdor `yield`, kështu që elementet kthehen një nga një pa krijuar
        kopje të radhës, dhe radha nuk ndryshon.
        """
        current = self._head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self):
        items = ", ".join(repr(v) for v in self)
        return f"Queue(head -> [{items}] <- tail)"
