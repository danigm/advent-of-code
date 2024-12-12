import math
from base import Problem


example = """
AAAA
BBCD
BBCC
EEEC
"""

example2 = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""

example3 = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

example4 = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""

example5 = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""


class Plot:
    def __init__(self, c):
        self.c = c
        self.region = set()
        self.edges = set()
        self.limits = [[], []]

    def area(self):
        return len(self.region)

    def perimeter(self):
        total = len(self.region) * 4
        edges = len(self.edges)
        return total - edges

    def _lines(self, points, order):
        a, b, c = order
        points = list(sorted(points, key=lambda i: (i[a], i[b], i[c])))

        l = 1
        # first one
        pd, pi, pj = points[0]
        for (nd, ni, nj) in points[1:]:

            # ordering by i
            if a == 1:
                diff_line = ni != pi
                diff = pj - nj
            # ordering by j
            else:
                diff_line = nj != pj
                diff = pi - ni

            # Detect a new line!
            # * different direction
            # * different line
            # * distance != 1
            if nd != pd or diff_line or math.fabs(diff) != 1:
                l += 1
            pd, pi, pj = nd, ni, nj
        return l

    def sides(self):
        # Order by i
        v = self._lines(self.limits[0], (1, 0, 2))
        # Order by j
        h = self._lines(self.limits[1], (2, 0, 1))
        return v + h

    def __str__(self):
        a = self.area()
        p = self.perimeter()
        s = self.sides()
        region = self.region
        return f"{self.c} {a}:{p}:{s} {region}"

    def __repr__(self):
        return str(self)


def test_part1():
    p = D12(example)
    assert p.solve_p1() == 140
    p = D12(example2)
    assert p.solve_p1() == 772
    p = D12(example3)
    assert p.solve_p1() == 1930


def test_part2():
    p = D12(example)
    assert p.solve_p2() == 80
    p = D12(example2)
    assert p.solve_p2() == 436
    p = D12(example4)
    assert p.solve_p2() == 236
    p = D12(example5)
    assert p.solve_p2() == 368
    p = D12(example3)
    assert p.solve_p2() == 1206


class D12(Problem):
    def solve_p1(self):
        n = 0
        for p in self.data:
            n += p.area() * p.perimeter()
        return n

    def solve_p2(self):
        n = 0
        for p in self.data:
            n += p.area() * p.sides()
        return n

    def adjacents(self, c, pos, data, plot=None, prev=None):
        i, j = pos
        if plot == None:
            plot = Plot(c)

        if prev:
            pi, pj = prev
            limit, li = (pj, i, j), 1
            if i != pi:
                limit, li = (pi, i, j), 0

        if i < 0 or j < 0:
            plot.limits[li].append(limit)
            return plot
        try:
            v = data[i][j]
        except IndexError:
            plot.limits[li].append(limit)
            return plot

        if v != c:
            plot.limits[li].append(limit)
            return plot

        if (i, j) in plot.region:
            plot.edges.add((prev, (i, j)))
            return plot

        plot.region.add((i, j))
        if prev:
            plot.edges.add((prev, (i, j)))
        self.adjacents(c, (i+1, j), data, plot, (i, j))
        self.adjacents(c, (i-1, j), data, plot, (i, j))
        self.adjacents(c, (i, j+1), data, plot, (i, j))
        self.adjacents(c, (i, j-1), data, plot, (i, j))
        
        return plot

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())

        plots = []
        visited = set()
        current_plot = []
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                if (i, j) in visited:
                    continue
                p = self.adjacents(c, (i, j), data)
                visited |= p.region
                plots.append(p)

        return plots


if __name__ == "__main__":
    print("Day 12: Garden Groups")

    p = D12("d12.data")
    print(p.solve_p1())
    print(p.solve_p2())
