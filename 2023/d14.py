from base import Problem


example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


example2 = """
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""


North = 0
South = 1
Left = 2
Right = 3


def test_part1():
    p = D14(example)
    assert len(p.rocks) == 35
    assert (0, 0) in p.rocks
    assert (0, 1) not in p.rocks
    assert p.to_str().strip() == example.strip()
    p.tilt(North)
    assert p.to_str().strip() == example2.strip()
    assert p.solve_p1() == 136


def test_part2():
    p = D14(example)
    assert p.solve_p2() == 0


class Rock:
    def __init__(self, r, c):
        self.initial = (r, c)
        self.pos = (r, c)

    @property
    def r(self):
        return self.pos[0]

    @property
    def c(self):
        return self.pos[1]

    def is_rounded(self):
        return False

    def is_solid(self):
        return not self.is_rounded()

    def __eq__(self, other):
        return self.pos == other.pos


class Rounded(Rock):
    def is_rounded(self):
        return True


class D14(Problem):
    def solve_p1(self):
        return 0

    def solve_p2(self):
        return 0

    def to_str(self):
        ss = []
        for r in range(self.rows):
            s = []
            for c in range(self.columns):
                s.append(self.rocks.get((r, c), "."))
            ss.append("".join(s))
        return "\n".join(ss)

    def tilt(self, direction=North):
        rocks = list(self.rocks.keys())
        # TODO: sort rocks depending on the tilt direction
        for (r, c) in rocks:
            rock = self.rocks.pop((r, c))
            # TODO: move the rock until other rock is found or the edge
            # place in the new position
            self.rocks[(r, c)] = rock

    def parseinput(self, lines):
        data = super().parseinput(lines)
        self.rows = len(data)
        self.columns = len(data[0])
        self.rocks = {}

        for r, line in enumerate(data):
            for c, s in enumerate(line):
                if s == ".":
                    continue
                self.rocks[(r, c)] = s

        return data


if __name__ == "__main__":
    print("Day 14: Parabolic Reflector Dish")

    p = D14("d14.data")
    print(p.solve_p1())
    print(p.solve_p2())
