from functools import lru_cache
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


ex_north = """
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


ex_south = """
.....#....
....#....#
...O.##...
...#......
O.O....O#O
O.#..O.#.#
O....#....
OO....OO..
#OO..###..
#OO.O#...O
"""


ex_west = """
O....#....
OOO.#....#
.....##...
OO.#OO....
OO......#.
O.#O...#.#
O....#OO..
O.........
#....###..
#OO..#....
"""


ex_east = """
....O#....
.OOO#....#
.....##...
.OO#....OO
......OO#.
.O#...O#.#
....O#..OO
.........O
#....###..
#..OO#....
"""


cycle1 = """
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....
"""

cycle2 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O
"""


cycle3 = """
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
"""


North = 0
South = 1
West = 2
East = 3


def test_part1():
    p = D14(example)
    assert p.solve_p1() == 136


def test_part2():
    print("Test part2")
    p = D14(example)
    n, tilted = p.tilt(p.data, North)
    assert n == 136
    assert p.to_str(tilted).strip() == ex_north.strip()

    n, tilted = p.tilt(p.data, South)
    assert n == 4 + 2*2 + 3*4 + 4 + 5*2 + 6*4 + 8
    assert p.to_str(tilted).strip() == ex_south.strip()

    n, tilted = p.tilt(p.data, West)
    assert n == 2 + 3 + 4*3 + 5*2 + 6*2 + 7*4 + 9*3 + 10
    assert p.to_str(tilted).strip() == ex_west.strip()

    n, tilted = p.tilt(p.data, East)
    assert n == 2 + 3 + 4*3 + 5*2 + 6*2 + 7*4 + 9*3 + 10
    assert p.to_str(tilted).strip() == ex_east.strip()

    n, c1 = p.cycle(p.data)
    assert p.to_str(c1).strip() == cycle1.strip()
    n, c2 = p.cycle(c1)
    assert p.to_str(c2).strip() == cycle2.strip()
    n, c3 = p.cycle(c2)
    assert p.to_str(c3).strip() == cycle3.strip()

    assert p.solve_p2() == 64


class D14(Problem):
    def solve_p1(self):
        return self.tilt(self.data, North)[0]

    def solve_p2(self):
        """
        Iterate 1 million times and look for a cycle. Then stop and calculate
        just the rest, if we repeat the cycle N times, we'll be in the same
        position, so no need to calculate more than that.
        """

        times = 1_000_000_000
        d = self.data
        repeat = 0
        visited = {}
        while times:
            n, d = self.cycle(d)
            s = self.to_str(d)
            if s in visited:
                # dead end
                break
            visited[s] = repeat
            repeat += 1
            times -= 1

        diff = times % (repeat - visited[s]) - 1
        while diff:
            n, d = self.cycle(d)
            s = self.to_str(d)
            diff -= 1
        return n

    def to_str(self, data):
        ret = []

        for row in data:
            ret.append("".join(c for c in row))

        return "\n".join(ret)

    @lru_cache(maxsize=None)
    def cycle(self, data):
        _, t1 = self.tilt(data, North)
        _, t2 = self.tilt(t1, West)
        _, t3 = self.tilt(t2, South)
        n, t4 = self.tilt(t3, East)

        return n, t4

    @lru_cache(maxsize=None)
    def tilt(self, data, direction=North):
        R = len(data)
        C = len(data[0])
        ndata = [list("." * C) for i in range(R)]

        L = R
        if direction == North:
            L = R
        elif direction == South:
            L = 1

        n = 0
        for i in range(R):
            if direction in [West, East]:
                load = L - i
            else:
                load = L
            if direction == West:
                p = 0
            else:
                p = -1

            for j in range(C):
                ci, cj = i, j
                oi, oj = i, L - load
                if direction == North:
                    ci, cj = j, i
                    oi, oj = L - load, i
                elif direction == South:
                    ci, cj = -(j + 1), i
                    oi, oj = -load, i
                elif direction == West:
                    ci, cj = i, j
                    oi, oj = i, p
                else:
                    ci, cj = i, -(j+1)
                    oi, oj = i, p

                rock = data[ci][cj]
                if rock == "#":
                    # solid rock
                    if direction == South:
                        load = L + (j + 1)
                    elif direction == North:
                        load = L - (j + 1)
                    elif direction == West:
                        p = cj + 1
                    else:
                        p = cj - 1
                    ndata[ci][cj] = "#"
                    continue

                if rock == "O":
                    n += load
                    # rounded rock
                    ndata[oi][oj] = "O"
                    if direction == South:
                        load += 1
                    elif direction == North:
                        load -= 1
                    elif direction == West:
                        p += 1
                    else:
                        p -= 1

        return n, tuple(tuple(i) for i in ndata)

    def parseinput(self, lines):
        data = tuple(tuple(i.strip()) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 14: Parabolic Reflector Dish")

    p = D14("d14.data")
    print(p.solve_p1())
    print(p.solve_p2())
