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
    assert p.solve_p2(6) == 16
    assert p.solve_p2(7) == 22
    assert p.solve_p2(10) == 50
    assert p.solve_p2(50) == 1594
    assert p.solve_p2(100) == 6536
    assert p.solve_p2(500) == 167004


class D21(Problem):
    def solve_p1(self, steps=64):
        return self.count_reach(steps)

    def solve_p2(self, steps=26501365):
        return self.count_reach(steps, True)

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
            reach = nr - set(i for i in explored)

        if initial_steps % 2:
            x = set(i for i in explored if explored[i] % 2 == 0)
        else:
            x = set(i for i in explored if explored[i] % 2)

        return len(reach) + len(x)

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

        for i in lines:
            i = i.strip()
            if not i:
                continue
            rows += 1
            cols = 0
            row = []
            for t in i:
                cols += 1
                if t == "S":
                    self.start = (rows - 1, cols - 1)
                    t = "."
                row.append(t)
            data.append(row)

        self.rows = rows
        self.cols = cols
        return data


if __name__ == "__main__":
    print("Day 21: Step Counter")

    p = D21("d21.data")
    print(p.solve_p1())
    print(p.solve_p2())
