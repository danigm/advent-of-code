from base import Problem
from collections import defaultdict


example = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""


def test_part1():
    p = D08(example)
    assert p.solve_p1() == 14


def test_part2():
    p = D08(example)
    assert p.solve_p2() == 34


class D08(Problem):
    def antinodes(self, a, b, extend=False):
        x1, y1 = a
        x2, y2 = b
        xd = x2 - x1
        yd = y2 - y1

        n1 = (x1 - xd, y1 - yd)
        n2 = (x2 + xd, y2 + yd)
        v1 = self.valid(n1)
        v2 = self.valid(n2)
        i = 2

        nodes = []
        while v1 or v2:
            if v1:
                nodes.append(n1)
            if v2:
                nodes.append(n2)

            if not extend:
                break

            n1 = (x1 - xd * i, y1 - yd * i)
            n2 = (x2 + xd * i, y2 + yd * i)
            v1 = self.valid(n1)
            v2 = self.valid(n2)
            i += 1

        return nodes

    def valid(self, node):
        i, j = node
        if i < 0 or j < 0:
            return False
        if i > self.height or j > self.width:
            return False
        return True

    def solve_p1(self):
        self.nodes = defaultdict(list)
        for k, v in self.data.items():
            if k == ".":
                continue
            for i, p in enumerate(v):
                for j in v[i+1:]:
                    nodes = self.antinodes(p, j)
                    self.nodes[k] += nodes

        # Unique values
        n = set()
        for v in self.nodes.values():
            n = n | set(v)

        return len(n)

    def solve_p2(self):
        self.nodes = defaultdict(list)
        for k, v in self.data.items():
            if k == ".":
                continue
            for i, p in enumerate(v):
                for j in v[i+1:]:
                    nodes = self.antinodes(p, j, extend=True)
                    self.nodes[k] += nodes + [p, j]

        # Unique values
        n = set()
        for v in self.nodes.values():
            n = n | set(v)

        return len(n)

    def parseinput(self, lines):
        data = defaultdict(list)
        self.width = 0
        self.height = 0

        for i, line in enumerate(i.strip() for i in lines if i.strip()):
            self.width = i
            for j, c in enumerate(line):
                self.height = j
                data[c].append((i, j))

        return data


if __name__ == "__main__":
    print("Day 08: Resonant Collinearity")

    p = D08("d08.data")
    print(p.solve_p1())
    print(p.solve_p2())
