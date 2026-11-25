"""Menyja kryesore e projektit "Stack & Queue from Scratch".

Përgjegjëse: Blenda Abazi

Ekzekutimi: python main.py
"""

from demos import bracket_matching, task_scheduler

MENU = """
==========================================
   Stack & Queue from Scratch
==========================================
  1. Kontrolli i kllapave   (Stack, LIFO)
  2. Planifikimi i detyrave (Queue, FIFO)
  0. Dalje
"""

DEMOS = {
    "1": bracket_matching.main,
    "2": task_scheduler.main,
}


def main():
    while True:
        print(MENU)
        try:
            choice = input("Zgjedhja: ").strip()
        except EOFError:
            break
        if choice == "0":
            break
        demo = DEMOS.get(choice)
        if demo is None:
            print("Zgjedhje e pavlefshme. Shkruaj 1, 2 ose 0.")
            continue
        print()
        demo()
    print("Mirupafshim!")


if __name__ == "__main__":
    main()
