import math
from base import Problem


example = """
3   4
4   3
2   5
1   3
3   9
3   3
"""


def test_part1():
    p = D01(example)
    assert p.solve_p1() == 11


def test_part2():
    p = D01(example)
    assert p.solve_p2() == 31


class D01(Problem):
    def solve_p1(self):
        p1, p2 = self.data
        return sum(int(math.fabs(i - j)) for (i, j) in zip(sorted(p1), sorted(p2)))

    def solve_p2(self):
        p1, p2 = self.data
        similarity = (i * p2.count(i) for i in p1)
        return sum(similarity)

    def parseinput(self, lines):
        data = [], []
        for i in lines:
            if not i.strip():
                continue
            n1, n2 = i.split()
            n1 = int(n1)
            n2 = int(n2)
            data[0].append(n1)
            data[1].append(n2)
        
        return data


if __name__ == "__main__":
    print("Day 01: Historian Hysteria")

    p = D01("d01.data")
    print(p.solve_p1())
    print(p.solve_p2())
