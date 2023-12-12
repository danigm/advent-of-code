import itertools
from base import Problem


example = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""


def test_part1():
    p = D11(example)
    assert len(p.galaxies) == 9
    assert p.emptyrows == [3, 7]
    assert p.emptycols == [2, 5, 8]
    assert p.galaxies[0] == [0, 3]
    assert p.galaxies[1] == [1, 7]
    assert p.galaxies[2] == [2, 0]
    assert p.galaxies[3] == [4, 6]
    p.expand()
    assert p.galaxies[0] == [0, 4]
    assert p.galaxies[1] == [1, 9]
    assert p.galaxies[2] == [2, 0]
    assert p.galaxies[3] == [5, 8]

    assert p.distance(p.galaxies[4], p.galaxies[8]) == 9
    assert p.distance(p.galaxies[0], p.galaxies[6]) == 15
    assert p.distance(p.galaxies[2], p.galaxies[5]) == 17
    assert p.distance(p.galaxies[7], p.galaxies[8]) == 5

    assert len(p.pairs()) == 36

    p = D11(example)
    assert p.solve_p1() == 374


def test_part2():
    p = D11(example)
    p.expand(10)
    assert len(p.pairs()) == 36
    assert sum(p.distance(*i) for i in p.pairs()) == 1030
    p = D11(example)
    p.expand(100)
    assert sum(p.distance(*i) for i in p.pairs()) == 8410


class D11(Problem):
    def solve_p1(self):
        self.expand()
        return sum(self.distance(*p) for p in self.pairs())

    def solve_p2(self):
        self.expand(1_000_000)
        return sum(self.distance(*p) for p in self.pairs())

    def pairs(self):
        return list(itertools.combinations(self.galaxies, 2))

    def distance(self, p1, p2):
        r1, c1 = p1
        r2, c2 = p2
        d = abs(r2 - r1) + abs(c2 - c1)

        return d

    def visualize(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if [r, c] in self.galaxies:
                    print("#", end="")
                else:
                    print(".", end="")

    def expand(self, time=2):
        """
        Expand the universe, any row or column without galaxies is
        expanded, twice as big.
        """

        if self.expanded:
            return

        for r in reversed(self.emptyrows):
            for g in self.galaxies:
                if g[0] > r:
                    g[0] += time - 1

        for c in reversed(self.emptycols):
            for i, g in enumerate(self.galaxies):
                if g[1] > c:
                    g[1] += time - 1

        self.rows += len(self.emptyrows) * (time - 1)
        self.columns += len(self.emptycols) * (time - 1)
        self.expanded = True


    def parseinput(self, lines):
        data = super().parseinput(lines)

        self.expanded = False
        self.rows = 0
        self.columns = 0
        self.universe = data
        self.galaxies = []
        # material rows and columns, rows and colums with some galaxy
        # in it
        self.mrows = []
        self.mcols = []

        self.rows = len(self.universe)
        self.columns = len(self.universe[0])

        for r, row in enumerate(self.universe):
            for c, column in enumerate(row):
                if column == "#":
                    self.mrows.append(r)
                    self.mcols.append(c)
                    self.galaxies.append([r, c])

        self.emptyrows = [i for i in range(len(self.universe)) if i not in self.mrows]
        self.emptycols = [i for i in range(len(self.universe[0])) if i not in self.mcols]

        return data


if __name__ == "__main__":
    print("Day 11: Cosmic Expansion")

    p = D11("d11.data")
    print(p.solve_p1())
    p = D11("d11.data")
    print(p.solve_p2())
