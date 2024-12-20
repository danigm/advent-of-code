from collections import defaultdict
from base import Problem


example = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_part1():
    p = D20(example)
    assert p.solve_p1(0) == 44


def test_part2():
    p = D20(example)
    assert p.solve_p2(0, 2) == 44
    n = 32 + 31 + 29 + 39 + 25 + 23 + 20 + 19 + 12 + 14 + 12 + 22 + 4 + 3
    assert p.solve_p2(50, 20) == n


def evaluate(start, end, vertex):
    r = [start]

    v = start
    visited = set()
    while v != end:
        visited.add(v)
        i, j = v
        p1, p2, p3, p4 = (0,  1), (0, -1), ( 1, 0), (-1, 0)
        for (pi, pj) in (p1, p2, p3, p4):
            m = i + pi, j + pj
            if m in vertex and m not in visited:
                r.append(m)
                v = m
                break

    return r


def calc_dist(v, limit=20):
    r = defaultdict(list)
    for n, p1 in enumerate(v):
        p1i, p1j = p1
        for p2 in v[n+2:]:
            p2i, p2j = p2
            di = p2i - p1i if p2i > p1i else p1i - p2i
            dj = p2j - p1j if p2j > p1j else p1j - p2j
            d = di + dj
            if d > limit:
                continue
            r[(d, p1)].append(p2)
    return r


def cheats(v, n=2):
    c = defaultdict(list)
    for (i, j) in v:
        p1, p2, p3, p4 = (0,  1), (0, -1), ( 1, 0), (-1, 0)
        for (pi, pj) in (p1, p2, p3, p4):
            m1i, m1j = i + pi, j + pj
            m2i, m2j = m1i + pi, m1j + pj
            if (m2i, m2j) in v and (m1i, m1j) not in v:
                c[(i, j)].append((m2i, m2j))
    return c


class D20(Problem):
    def solve_p1(self, x=100):
        v = self.v
        m = self.data

        possible_cheats = cheats(v)
        positions = {p: i for i, p in enumerate(m)}
        real_cheats = []
        for p, i in positions.items():
            if p not in possible_cheats:
                continue
            for c in possible_cheats[p]:
                n = positions[c]
                # Cheat backward?
                if n < i:
                    continue
                real_cheats.append(n - i - 2)
        return len([i for i in real_cheats if i >= x])

    def solve_p2(self, x=100, s=20):
        v = self.v
        m = self.data
        positions = {p: i for i, p in enumerate(m)}
        l = len(m) - 1
        distances = calc_dist(m, s)
        real_cheats = {}
        for p1, i in positions.items():
            for d in range(2, s + 1):
                for p2 in distances[(d, p1)]:
                    n = positions[p2]
                    # Cheat backward?
                    if n < i or (n - i - d) == 0:
                        continue
                    diff = (n - i - d)
                    real_cheats[(p1, p2)] = diff
        out = [i for k, i in real_cheats.items() if i >= x]
        return len(out)

    def parseinput(self, lines):
        self.s, self.e = (0, 0), (0, 0)
        self.map = []
        data = []
        i = 0
        for line in lines:
            l = line.strip()
            if not l:
                continue
            self.map.append(l)
            for j, c in enumerate(l):
                if c in "SE.":
                    data.append((i, j))
                if c == "S":
                    self.s = (i, j)
                if c == "E":
                    self.e = (i, j)
            i += 1

        self.v = set(data)

        data = evaluate(self.s, self.e, self.v)

        return data


if __name__ == "__main__":
    print("Day 20: Race Condition")

    p = D20("d20.data")
    print(p.solve_p1())
    print(p.solve_p2())
