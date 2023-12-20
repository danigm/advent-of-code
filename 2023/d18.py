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
L 6 (#70c710)
U 5 (#0dc571)
R 6 (#5713f0)
D 5 (#d2c081)
"""


def test_part1():
    p = D18(example)
    assert sum([h.n for h in p.holes]) == 38
    print(p.area([(0,0), (0,6), (5,6), (5,0), (0,0)]))
    assert p.solve_p1() == 62

    p = D18(example2)


def test_part2():
    p = D18(example)
    assert p.solve_p2() == 952408144115


class Hole:
    def __init__(self, line=None):
        self.dir = "U"
        self.n = 1
        self.parse_line(line)

    def parse_line(self, line):
        if line is None:
            return

        dirs = {"0": "R", "1": "D", "2": "L", "3": "U"}

        d, n, color = line.split()
        self.dir = d
        self.n = int(n)
        self.color = color[2:-1]
        self.nn = int(self.color[:5], base=16)
        self.nd = dirs[self.color[-1]]

    def __repr__(self):
        return f"{self.dir} {self.n} (#{self.color})"


class D18(Problem):
    def solve_p1(self):
        r = sum([h.n for h in self.holes if h.dir == "R"])
        d = sum([h.n for h in self.holes if h.dir == "D"])
        l = sum([h.n for h in self.holes if h.dir == "L"])
        u = sum([h.n for h in self.holes if h.dir == "U"])
        return self.area(self.vertex) + r + d + 1

    def solve_p2(self):
        r = sum([h.nn for h in self.holes if h.nd == "R"])
        d = sum([h.nn for h in self.holes if h.nd == "D"])
        l = sum([h.nn for h in self.holes if h.nd == "L"])
        u = sum([h.nn for h in self.holes if h.nd == "U"])
        return self.area(self.vertex2) + r + d + 1

    # https://www.mathsisfun.com/geometry/area-irregular-polygons.html
    def area(self, coords):
        t=0
        for count in range(len(coords)-1):
            y = coords[count+1][1] + coords[count][1]
            x = coords[count+1][0] - coords[count][0]
            z = y * x
            t += z

        mr = sorted(coords)[-1][0]
        mc = sorted(coords, key=lambda x: x[1])[-1][1]
        return int(t/2)

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())

        self.holes = []
        self.holes = [Hole(i) for i in data]
        self.vertex = [(0, 0)]
        self.vertex2 = [(0, 0)]
        r, c = 0, 0
        r2, c2 = 0, 0
        for h in self.holes:
            i = h.n
            if h.dir == "R":
                nr, nc = r, c+i
            if h.dir == "D":
                nr, nc = r+i, c
            if h.dir == "U":
                nr, nc = r-i, c
            if h.dir == "L":
                nr, nc = r, c-i
            r, c = nr, nc
            self.vertex.append((r, c))

            i = h.nn
            if h.nd == "R":
                nr, nc = r2, c2+i
            if h.nd == "D":
                nr, nc = r2+i, c2
            if h.nd == "U":
                nr, nc = r2-i, c2
            if h.nd == "L":
                nr, nc = r2, c2-i
            r2, c2 = nr, nc
            self.vertex2.append((r2, c2))

        return data


if __name__ == "__main__":
    print("Day 18: Lavaduct Lagoon")

    p = D18("d18.data")
    print(p.solve_p1())
    print(p.solve_p2())
