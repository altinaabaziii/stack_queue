"""Demo: planifikimi i detyrave me Round-Robin, duke përdorur Queue.

Përgjegjëse: Blenda Abazi

Kështu e ndan sistemi operativ CPU-në mes proceseve: secili proces merr me
radhë një copë të vogël kohe (quantum). Nëse nuk mbaron, del nga CPU-ja dhe
rikthehet në fund të radhës, që të mos i bllokojë të tjerët.

Algoritmi:
  1. Fut të gjitha detyrat në radhë (push), sipas rendit të ardhjes.
  2. Sa kohë radha nuk është bosh:
       - merr detyrën e parë (pop);
       - ekzekutoje për min(quantum, koha e mbetur);
       - nëse i ka mbetur kohë -> push përsëri në fund të radhës;
         përndryshe -> regjistro kohën e përfundimit.

Radha është zgjedhja e natyrshme, sepse detyra që ka pritur më gjatë
shërbehet e para (FIFO), dhe kështu asnjë detyrë nuk mbetet pa CPU.

          pop                                   push (nëse s'ka mbaruar)
   CPU <------ [ A ] -> [ B ] -> [ C ] <----------------------------+
    |                                                               |
    +---------------------------------------------------------------+

Kompleksiteti: çdo hap bën një pop dhe ndoshta një push, pra O(1) për hap.
Numri i hapave është shuma e ceil(kohë / quantum) për të gjitha detyrat.

Ekzekutimi: python -m demos.task_scheduler
"""

from dataclasses import dataclass

from structures.queue import Queue


@dataclass
class Task:
    """Një detyrë (proces) që pret CPU-në."""

    name: str
    burst: int        # koha totale që i duhet detyrës
    remaining: int    # koha që i ka mbetur ende


@dataclass
class FinishedTask:
    """Rezultati për një detyrë të përfunduar."""

    name: str
    burst: int
    finish_time: int   # momenti kur mbaroi (të gjitha nisin në kohën 0)

    @property
    def waiting_time(self):
        """Koha që detyra ka pritur në radhë pa punuar."""
        return self.finish_time - self.burst


def round_robin(tasks, quantum, verbose=False):
    """Simulon Round-Robin dhe kthen detyrat në rendin që përfunduan.

    `tasks` është një varg çiftesh (emri, koha). Kthen listë me FinishedTask.
    Kur `verbose=True` shtyp çdo hap dhe përmbajtjen e radhës.
    """
    if quantum <= 0:
        raise ValueError("quantum duhet të jetë numër pozitiv")

    queue = Queue()
    for name, burst in tasks:
        if burst <= 0:
            raise ValueError(f"koha e detyrës '{name}' duhet të jetë pozitive")
        queue.push(Task(name, burst, burst))

    if verbose:
        print(f"  Radha fillestare: {_queue_str(queue)}   (quantum = {quantum})")

    clock = 0
    finished = []
    while not queue.is_empty():
        task = queue.pop()
        run = min(quantum, task.remaining)
        start = clock
        clock += run
        task.remaining -= run

        if task.remaining > 0:
            queue.push(task)  # s'ka mbaruar: kthehet në fund të radhës
            status = f"mbeten {task.remaining}, kthehet në fund"
        else:
            finished.append(FinishedTask(task.name, task.burst, clock))
            status = "MBAROI"

        if verbose:
            print(f"  t={start:>2}..{clock:<2}  {task.name} punon {run}  "
                  f"({status})  ->  radha: {_queue_str(queue)}")

    return finished


def _queue_str(queue):
    return " ".join(f"{t.name}({t.remaining})" for t in queue) or "(bosh)"


def show_summary(finished):
    """Shtyp tabelën e përfundimit dhe kohën mesatare të pritjes."""
    print(f"\n  {'Detyra':<8}{'Koha':>6}{'Mbaroi':>8}{'Priti':>7}")
    for t in finished:
        print(f"  {t.name:<8}{t.burst:>6}{t.finish_time:>8}{t.waiting_time:>7}")
    if finished:
        avg = sum(t.waiting_time for t in finished) / len(finished)
        print(f"  Pritja mesatare: {avg:.2f}")


EXAMPLE_TASKS = [("A", 5), ("B", 3), ("C", 1), ("D", 4)]
EXAMPLE_QUANTUM = 2


def _read_tasks():
    """Lexon detyrat nga përdoruesi, p.sh. 'A 5, B 3, C 1'. Kthen None për dalje."""
    try:
        line = input("Detyrat (p.sh. 'A 5, B 3, C 1', Enter bosh për të dalë): ")
        if not line.strip():
            return None
        tasks = []
        for part in line.split(","):
            name, burst = part.split()
            tasks.append((name, int(burst)))
        quantum = int(input("Quantum: "))
    except EOFError:
        return None
    except ValueError:
        print("  Format i gabuar. Shembull: A 5, B 3, C 1")
        return []
    return tasks, quantum


def main():
    print("=== Planifikimi Round-Robin me Queue ===\n")

    print(f"Shembull me detyrat {EXAMPLE_TASKS}:")
    show_summary(round_robin(EXAMPLE_TASKS, EXAMPLE_QUANTUM, verbose=True))

    print("\nProvo detyrat e tua:")
    while True:
        data = _read_tasks()
        if data is None:
            break
        if not data:
            continue
        tasks, quantum = data
        try:
            show_summary(round_robin(tasks, quantum, verbose=True))
        except ValueError as e:
            print(f"  GABIM: {e}")
        print()


if __name__ == "__main__":
    main()
