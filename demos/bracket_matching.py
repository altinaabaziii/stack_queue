"""Demo: kontrolli i kllapave (bracket matching) me Stack.

Përgjegjëse: Altina Abazi

Algoritmi:
  1. Lexo tekstin karakter për karakter.
  2. Kur gjen kllapë hapëse ( [ {  -> bëj push në stivë (bashkë me pozicionin).
  3. Kur gjen kllapë mbyllëse ) ] } :
       - nëse stiva është bosh       -> gabim: mbyllëse pa hapëse;
       - përndryshe bëj pop; nëse kllapa e nxjerrë nuk përputhet -> gabim.
  4. Në fund, nëse stiva nuk është bosh -> gabim: kllapë e pambyllur.

Stiva funksionon sepse kllapa e fundit e hapur duhet të mbyllet e para (LIFO).
Kompleksiteti: O(n) kohë, O(n) memorie, ku n është gjatësia e tekstit.

Ekzekutimi: python -m demos.bracket_matching
"""

from dataclasses import dataclass

from structures.stack import Stack

OPENING = "([{"
CLOSING = ")]}"  # CLOSING[i] është çifti i OPENING[i]


@dataclass
class BracketResult:
    """Rezultati i kontrollit: a është teksti i balancuar dhe ku është gabimi."""

    balanced: bool
    position: int = -1   # indeksi i gabimit (-1 kur s'ka gabim)
    message: str = "Kllapat janë të balancuara."


def check_brackets(text, verbose=False):
    """Kontrollon nëse kllapat në `text` janë të balancuara.

    Kur `verbose=True` shtyp çdo hap dhe përmbajtjen e stivës.
    """
    stack = Stack()  # ruan çifte (kllapa, pozicioni)

    for i, ch in enumerate(text):
        if ch in OPENING:
            stack.push((ch, i))
            if verbose:
                _trace(i, ch, "push", stack)

        elif ch in CLOSING:
            if stack.is_empty():
                return BracketResult(
                    False, i,
                    f"Kllapa mbyllëse '{ch}' në pozicionin {i} nuk ka kllapë hapëse.",
                )
            open_ch, open_pos = stack.pop()
            if verbose:
                _trace(i, ch, "pop ", stack)
            expected = CLOSING[OPENING.index(open_ch)]
            if ch != expected:
                return BracketResult(
                    False, i,
                    f"Pritej '{expected}' (për '{open_ch}' në pozicionin {open_pos}), "
                    f"por u gjet '{ch}' në pozicionin {i}.",
                )

    if not stack.is_empty():
        open_ch, open_pos = stack.peek()
        return BracketResult(
            False, open_pos,
            f"Kllapa '{open_ch}' në pozicionin {open_pos} nuk u mbyll kurrë.",
        )

    return BracketResult(True)


def _trace(i, ch, action, stack):
    contents = " ".join(c for c, _ in stack) or "(bosh)"
    print(f"  [{i:>2}] '{ch}'  {action}  ->  stiva (maja majtas): {contents}")


def show_result(text, result):
    """Shtyp tekstin dhe, nëse ka gabim, një shigjetë ^ nën pozicionin e tij."""
    print(f"  {text}")
    if result.balanced:
        print(f"  OK: {result.message}")
    else:
        print(f"  {' ' * result.position}^")
        print(f"  GABIM: {result.message}")


EXAMPLES = [
    "def f(a, b): return [a, {b: (a + b)}]",
    "if (x > 0 { print(x) }",
    "items[0] = (1, 2))",
    "{[()()]}",
    "((( [ ]",
]


def main():
    print("=== Kontrolli i kllapave me Stack ===\n")

    print("Hap pas hapi për shembullin '{[()]}':")
    show_result("{[()]}", check_brackets("{[()]}", verbose=True))

    print("\nShembuj të tjerë:")
    for text in EXAMPLES:
        print()
        show_result(text, check_brackets(text))

    print("\nShkruaj tekstin tënd (Enter bosh për të dalë):")
    while True:
        try:
            text = input("> ")
        except EOFError:
            break
        if not text:
            break
        show_result(text, check_brackets(text, verbose=True))


if __name__ == "__main__":
    main()
