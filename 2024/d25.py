import os
from io import StringIO
from base import Problem


example = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""


def test_part1():
    p = D25(example)
    locks, keys = p.data
    assert len(locks) == 2
    assert len(keys) == 3
    assert locks[0] == [0, 5, 3, 4, 3]
    assert locks[1] == [1, 2, 0, 5, 3]
    assert keys[0] == [5, 0, 2, 1, 3]
    assert keys[1] == [4, 3, 4, 0, 2]
    assert keys[2] == [3, 0, 2, 0, 1]
    assert p.solve_p1() == 3


def test_part2():
    p = D25(example)
    assert p.solve_p2() == 0


def fit(key, lock):
    for i in range(5):
        if key[i] + lock[i] > 5:
            return False
    return True


class D25(Problem):
    def solve_p1(self):
        locks, keys = self.data
        n = 0
        for k in keys:
            for l in locks:
                if fit(k, l):
                    n += 1
        return n

    def solve_p2(self):
        return 0

    def readinput(self):
        if not os.path.exists(self.input):
            input = StringIO(self.input)
            self.data = self.parseinput(input.read())
            return

        with open(self.input) as f:
            self.data = self.parseinput(f.read())

    def parseinput(self, data):
        locks = []
        keys = []
        patterns = data.split("\n\n")
        for p in patterns:
            lines = [i.strip() for i in p.split("\n") if i.strip()]
            if lines[0] == "#####":
                container = locks
                lines = lines[1:]
            else:
                container = keys
                lines = list(reversed(lines))[1:]

            k = [0, 0, 0, 0, 0]
            for c in range(5):
                for r, line in enumerate(lines):
                    if line[c] == ".":
                        k[c] = r
                        break

            container.append(k)

        return locks, keys


if __name__ == "__main__":
    print("Day 25: ")

    p = D25("d25.data")
    print(p.solve_p1())
    print(p.solve_p2())
