import re
from base import Problem


example = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""

example2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

MUL = re.compile(r"mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)")
MUL_DO = re.compile(r"(?P<do>do\(\))|(?P<dont>don't\(\))|mul\((?P<x>\d{1,3}),(?P<y>\d{1,3})\)")


def test_part1():
    p = D03(example)
    assert p.solve_p1() == 161


def test_part2():
    p = D03(example2)
    assert p.solve_p2() == 48


class D03(Problem):
    def solve_p1(self):
        r = 0
        for line in self.data:
            match = MUL.findall(line)
            for x, y in match:
                r += int(x) * int(y)
        return r

    def solve_p2(self):
        r = 0
        do = True
        for line in self.data:
            match = MUL_DO.findall(line)
            for ndo, ndont, x, y in match:
                if ndo:
                    do = True
                if ndont:
                    do = False
                if x and y and do:
                    r += int(x) * int(y)
        return r

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 03: Clumsy Crucible")

    p = D03("d03.data")
    print(p.solve_p1())
    print(p.solve_p2())
