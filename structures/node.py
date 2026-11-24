"""Nyja (Node): blloku bazë i listës së lidhur.

Përgjegjëse: Altina Abazi (përdoret nga Stack dhe Queue)

Në vend të listave të Python-it (list, deque), çdo element ruhet në një
nyje që mban vlerën dhe një referencë te nyja e radhës. Kështu shtimi dhe
heqja bëhen në O(1), pa zhvendosur elemente në memorie.
"""


class Node:
    """Një nyje e listës së lidhur njëdrejtimëshe."""

    __slots__ = ("value", "next")  # vetëm këto dy atribute, kursen memorie

    def __init__(self, value, next_node=None):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return f"Node({self.value!r})"
