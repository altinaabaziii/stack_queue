"""Stack: strukturë LIFO (Last In, First Out).

Përgjegjëse: Altina Abazi

Implementimi përdor listë të lidhur, ku maja (top) e Stack-ut është koka e listës:

    top
     |
     v
   [ C ] -> [ B ] -> [ A ] -> None

    push  -> shton nyje të re në krye          O(1)
    pop   -> heq nyjen nga kreu                 O(1)
    peek  -> lexon vlerën në krye pa e hequr    O(1)
"""

from structures.node import Node


class EmptyStackError(Exception):
    """Ngritet kur kërkohet pop ose peek nga një Stack i zbrazët."""


class Stack:
    """Stack i implementuar me listë të lidhur, pa koleksione të gatshme."""

    def __init__(self, items=None):
        self._top = None   # nyja në majë të Stack-ut
        self._size = 0     # numri i elementeve
        if items is not None:
            for item in items:
                self.push(item)

    def push(self, value):
        """Vendos `value` në majë të Stack-ut. O(1)"""
        self._top = Node(value, self._top)
        self._size += 1

    def pop(self):
        """Heq dhe kthen elementin në majë. O(1)

        Ngre EmptyStackError nëse Stack-u është i zbrazët.
        """
        if self.is_empty():
            raise EmptyStackError("pop nga Stack i zbrazët")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.value

    def peek(self):
        """Kthen elementin në majë pa e hequr. O(1)

        Ngre EmptyStackError nëse Stack-u është i zbrazët.
        """
        if self.is_empty():
            raise EmptyStackError("peek në Stack të zbrazët")
        return self._top.value

    def is_empty(self):
        """Kthen True nëse Stack-u nuk ka elemente. O(1)"""
        return self._top is None

    def __len__(self):
        return self._size

    def __iter__(self):
        """Iteron nga maja drejt fundit, në rendin që do të dilnin me pop.

        Përdor `yield`, kështu që elementet kthehen një nga një pa krijuar
        kopje të Stack-ut, dhe Stack-u nuk ndryshon.
        """
        current = self._top
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self):
        items = ", ".join(repr(v) for v in self)
        return f"Stack(top -> [{items}])"
