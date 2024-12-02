import math
from functools import partial
from base import Problem


example = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

example2 = """
48 46 47 49 51 54 56
1 1 2 3 4 5
1 2 3 4 5 5
5 1 2 3 4 5
1 4 3 2 1
1 6 7 8 9
1 2 3 4 3
9 8 7 6 7
"""


def test_part1():
    p = D02(example)
    assert p.solve_p1() == 2


def test_part2():
    p = D02(example)
    assert p.solve_p2() == 4
    p = D02(example2)
    assert p.solve_p2() == 8


class D02(Problem):
    def _safe(self, line, tolerance=0):
        """
        It's safe if:
        * The levels are either all increasing or all decreasing.
        * Any two adjacent levels differ by at least one and at most three.
        """

        prev = None
        incr = None
        failure = False
        for i, level in enumerate(line):
            if prev is None:
                prev = level
                continue

            diff = level - prev
            fdiff = math.fabs(diff)
            if fdiff < 1 or fdiff > 3:
                failure = True
                if tolerance == 0:
                    return False

            new_incr = (diff) > 0
            if incr is None:
                incr = new_incr
            if new_incr != incr:
                failure = True
                if tolerance == 0:
                    return False

            if failure:
                # Edge case, when it can be safe if the first one is
                # removed because of order change
                remove_first = False
                if i == 2:
                    remove_first = self._safe(line[1:], tolerance-1)

                return (self._safe(line[:i-1] + line[i:], tolerance-1) or
                        self._safe(line[:i] + line[i+1:], tolerance-1) or remove_first)

            prev = level

        return True

    def solve_p1(self):
        safe = list(filter(self._safe, self.data))
        return len(safe)

    def solve_p2(self):
        safe = list(filter(partial(self._safe, tolerance=1), self.data))
        return len(safe)

    def parseinput(self, lines):
        data = tuple(tuple(int(j) for j in i.strip().split()) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 02: Red-Nosed Reports")

    p = D02("d02.data")
    print(p.solve_p1())
    print(p.solve_p2())
