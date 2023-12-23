from base import Problem


example = """
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1():
    p = D21(example)
    assert p.solve_p1(6) == 16


def test_part2():
    p = D21(example)
    assert p.count_reach(6, True) == 16
    assert p.count_reach(7, True) == 22
    assert p.count_reach(10, True) == 50
    assert p.count_reach(50, True) == 1594
    assert p.count_reach(100, True) == 6536
    assert p.count_reach(500, True) == 167004


class D21(Problem):
    def solve_p1(self, steps=64):
        return self.count_reach(steps)

    def solve_p2(self, steps=26501365):
        # I was unable to find the solution to the second problem
        # Solved with the help of
        # https://raw.githubusercontent.com/CalSimmon/advent-of-code/main/2023/day_21/solution.py
        #
        # I don't fully understand this solution it's something related with
        # the specific input set, because this doesn works with the example
        # input, in that case what it works is:
        # return self.count_reach(steps, True)

        # Use quadratic formula to extrapolate
        goal = steps
        size = self.rows
        edge = size // 2
        # calculate the first three squares, to reach initial bound, and then
        # to reach the second and third expansion.
        # i=0, s -> (edge) -> |
        # i=1, s -> (edge) -> | -> (size) -> |
        # i=2, s -> (edge) -> | -> (size) -> | -> (size) -> |
        y = [self.count_reach((edge + i * size), True) for i in range(3)]
        # 202300 = (26501365 - 65) // 131
        # 26501365 isn't a random number. Our input is 131x131 tiles in size,
        # and 26501365 = 65 + (202300 * 131). 65 is the number of steps it
        # takes to get from the centre of the square to the edge, and 131 is
        # the number of steps it takes to traverse the whole square
        n = ((goal - edge) // size)

        # Use the quadratic formula to find the output at the large steps based
        # on the first three data points
        a = (y[2] - (2 * y[1]) + y[0]) // 2
        b = y[1] - y[0] - a
        c = y[0]
        return (a * n**2) + (b * n) + c

    def count_reach(self, steps, infinite=False):
        reach = set()
        reach.add(self.start)
        explored = {}
        initial_steps = steps

        i = 0
        while steps:
            steps -= 1
            i += 1

            nr = set()
            for r, c in reach:
                explored[(r, c)] = i
                possible = self.possible_pots(r, c, infinite)
                nr = nr | possible

            reach = nr - set(j for j in explored)

        if initial_steps % 2:
            x = set(i for i in explored if explored[i] % 2 == 0) | reach
        else:
            x = set(i for i in explored if explored[i] % 2) | reach

        return len(x)

    def inf_point(self, r, c):
        return r % self.rows, c % self.cols

    def possible_pots(self, r, c, infinite=False):
        pos = set()
        data = self.data

        # top
        nr, nc = r - 1, c
        if infinite:
            nr, nc = self.inf_point(nr, nc)
        if nr >= 0 and data[nr][nc] == ".":
            pos.add((r - 1, c))
        # bottom
        nr, nc = r + 1, c
        if infinite:
            nr, nc = self.inf_point(nr, nc)
        if nr < self.rows and data[nr][nc] == ".":
            pos.add((r + 1, c))
        # left
        nr, nc = r, c - 1
        if infinite:
            nr, nc = self.inf_point(nr, nc)
        if nc >= 0 and data[nr][nc] == ".":
            pos.add((r, c - 1))
        # right
        nr, nc = r, c + 1
        if infinite:
            nr, nc = self.inf_point(nr, nc)
        if nc < self.cols and data[nr][nc] == ".":
            pos.add((r, c + 1))

        return pos

    def parseinput(self, lines):
        data = []
        rows = 0
        cols = 0
        pots = set()

        lines = (i for i in lines if i.strip())
        for r, i in enumerate(lines):
            rows += 1
            cols = 0
            row = []
            for c, t in enumerate(i.strip()):
                cols += 1
                if t == "S":
                    self.start = (rows - 1, cols - 1)
                    t = "."
                if t != "#":
                    pots.add((r, c))
                row.append(t)
            data.append(row)

        self.rows = rows
        self.cols = cols
        self.pots = pots
        return data


if __name__ == "__main__":
    print("Day 21: Step Counter")

    p = D21("d21.data")
    print(p.solve_p1())
    print(p.solve_p2())
