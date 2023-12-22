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
    assert p.solve_p2() == 0


class D21(Problem):
    def solve_p1(self, steps=64):
        return self.count_reach(steps)

    def solve_p2(self):
        return 0

    def count_reach(self, steps):
        reach = set()
        reach.add(self.start)

        while steps:
            steps -= 1
            nr = set()
            for r, c in reach:
                nr = nr | self.possible_pots(r, c)
            reach = nr

        return len(reach)

    def possible_pots(self, r, c):
        pos = set()
        data = self.data

        # top
        nr, nc = r - 1, c
        if nr >= 0 and data[nr][nc] == ".":
            pos.add((nr, nc))
        # bottom
        nr, nc = r + 1, c
        if nr < self.rows and data[nr][nc] == ".":
            pos.add((nr, nc))
        # left
        nr, nc = r, c - 1
        if nc >= 0 and data[nr][nc] == ".":
            pos.add((nr, nc))
        # right
        nr, nc = r, c + 1
        if nc < self.cols and data[nr][nc] == ".":
            pos.add((nr, nc))

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
