import math
from base import Problem


example = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_d9_part1():
    p = D9(example)
    h = History("0 3 6 9 12 15")
    assert h.prediction() == 18
    h = History("1 3 6 10 15 21")
    assert h.prediction() == 28
    h = History("10 13 16 21 30 45")
    assert h.prediction() == 68

    assert p.solve_p1() == 114


def test_d9_part2():
    p = D9(example)
    h = History("0 3 6 9 12 15")
    assert h.past() == -3
    h = History("1 3 6 10 15 21")
    assert h.past() == 0
    h = History("10 13 16 21 30 45")
    assert h.past() == 5
    assert p.solve_p2() == 2


class History:
    def __init__(self, line):
        self.numbers = [int(i) for i in line.split()]

    def prediction(self, numbers=None):
        if numbers is None:
            numbers = self.numbers

        diffs = self.diffs(numbers)
        if [i for i in diffs if i]:
            return self.prediction(diffs) + numbers[-1]
        return numbers[-1]

    def past(self, numbers=None):
        """
        Just reverse the numbers and that works
        """
        if numbers is None:
            numbers = self.numbers
        return self.prediction(list(reversed(numbers)))

    def diffs(self, numbers):
        diffs = []
        for i in range(1, len(numbers)):
            diffs.append(numbers[i] - numbers[i - 1])

        return diffs


class D9(Problem):
    def solve_p1(self):
        return sum((i.prediction() for i in self.data))

    def solve_p2(self):
        return sum((i.past() for i in self.data))

    def parseinput(self, lines):
        data = super().parseinput(lines)
        data = [History(i) for i in data]
        return data


if __name__ == "__main__":
    print("Day 9: Mirage Maintenance")

    p = D9("d9.data")
    print(p.solve_p1())
    print(p.solve_p2())
