import re
from functools import cache
from base import Problem


example = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def test_part1():
    p = D19(example)
    assert p.solve_p1() == 6


def test_part2():
    p = D19(example)
    assert p.solve_p2() == 16


@cache
def possibles(design, patterns):
    n = 0
    if not design:
        return 1

    for i in patterns:
        if design.startswith(i):
            n += possibles(design[len(i):], patterns)

    return n


class D19(Problem):
    def solve_p1(self):
        towel = "|".join(self.patterns)
        r = re.compile(fr"^({towel})+$")

        p = 0
        for d in self.designs:
            if r.match(d):
                p += 1

        return p

    def solve_p2(self):
        p = 0
        for d in self.designs:
            p += possibles(d, tuple(self.patterns))
        return p

    def parseinput(self, lines):
        self.patterns = []
        self.designs = []
        for line in lines:
            l = line.strip()
            if not l:
                continue
            if "," in l:
                self.patterns = l.split(", ")
            else:
                self.designs.append(l)

        return self.patterns, self.designs


if __name__ == "__main__":
    print("Day 19: Linen Layout")

    p = D19("d19.data")
    print(p.solve_p1())
    print(p.solve_p2())
