from base import Problem


example = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""


def test_part1():
    p = D04(example)
    assert p.solve_p1() == 18


def test_part2():
    p = D04(example)
    assert p.solve_p2() == 9


class D04(Problem):
    def _look_for(self, i, j, di, dj, word="XMAS"):
        for c in word:
            if i < 0 or j < 0:
                return 0
            try:
                d = self.data[i][j]
            except IndexError:
                return 0

            if c != d:
                return 0
            i += di
            j += dj
        return 1

    def solve_p1(self):
        n = 0
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char == "X":
                    # Look for XMAS in every direction
                    d1 = self._look_for(i, j, 1, 0)
                    d2 = self._look_for(i, j, -1, 0)
                    d3 = self._look_for(i, j, 0, 1)
                    d4 = self._look_for(i, j, 0, -1)
                    d5 = self._look_for(i, j, 1, 1)
                    d6 = self._look_for(i, j, 1, -1)
                    d7 = self._look_for(i, j, -1, 1)
                    d8 = self._look_for(i, j, -1, -1)
                    n += d1 + d2 + d3 + d4 + d5 + d6 + d7 + d8
        return n

    def solve_p2(self):
        n = 0
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char == "A":
                    # Look for X-MAS in every direction
                    d1 = self._look_for(i-1, j-1, 1, 1, "MAS")
                    d2 = self._look_for(i+1, j-1, -1, 1, "MAS")
                    d3 = self._look_for(i-1, j+1, 1, -1, "MAS")
                    d4 = self._look_for(i+1, j+1, -1, -1, "MAS")
                    d = d1 + d2 + d3 + d4
                    if d == 2:
                        n += 1
        return n

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 04: Ceres Search")

    p = D04("d04.data")
    print(p.solve_p1())
    print(p.solve_p2())
