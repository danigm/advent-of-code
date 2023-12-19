import itertools
from base import Problem


example = """
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

example2 = """
R 6 (#70c710)
D 5 (#0dc571)
L 6 (#0dc571)
U 5 (#0dc571)
"""


def test_part1():
    p = D18(example2)
    assert sum([h.n for h in p.holes]) == 22
    polygon = [h.end for h in p.holes]
    assert p.area(polygon) == 42
    # polygon = [
    #     (0, 6), (5, 6), (5, 4),
    #     (7, 4), (7, 6), (9, 6), (9, 1),
    #     (7, 1), (7, 0), (5, 0), (5, 2),
    #     (2, 2), (2, 0), (0, 0)
    # ]
    # assert p.area(polygon) == 62

    p = D18(example)
    assert sum([h.n for h in p.holes]) == 38
    assert p.solve_p1() == 62


def test_part2():
    p = D18(example)
    assert p.solve_p2() == 0


class Hole:
    def __init__(self, line=None, start=(0, 0)):
        if line is None:
            self.dir = "X"
            self.n = 1
            self.color = "000000"
            self.r, self.g, self.b = 0, 0, 0
            self.start = start
            self.end = start
            return

        d, n, color = line.split()
        self.dir = d
        self.n = int(n)
        self.color = color[2:-1]
        self.r = int(self.color[0:2], base=16)
        self.g = int(self.color[2:4], base=16)
        self.b = int(self.color[4:6], base=16)
        self.start = start

        r, c = start
        n = self.n
        if d == "U":
            self.end = (r - n, c)
        elif d == "D":
            self.end = (r + n, c)
        elif d == "L":
            self.end = (r, c - n)
        elif d == "R":
            self.end = (r, c + n)

    def __repr__(self):
        return f"{self.dir} {self.n} (#{self.color})"


class D18(Problem):
    def solve_p1(self):
        polygon = [i.end for i in self.holes]
        return self.area(polygon)

    def solve_p2(self):
        return 0

    # https://www.mathsisfun.com/geometry/area-irregular-polygons.html
    def area(self, coords):
        print(coords)
        t=0
        for count in range(len(coords)-1):
            y = coords[count+1][1] + coords[count][1]
            x = coords[count+1][0] - coords[count][0]
            z = y * x
            print(count, x, y, z)
            t += z
        return int(abs(t/2))

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())

        self.holes = []
        pos = (0, 1)
        for i, line in enumerate(data):
            hole = Hole(line, pos)
            self.holes.append(hole)
            pos = hole.end

        return data


if __name__ == "__main__":
    print("Day 18: Lavaduct Lagoon")

    p = D18("d18.data")
    print(p.solve_p1())
    print(p.solve_p2())
