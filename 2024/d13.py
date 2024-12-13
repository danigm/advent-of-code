import re
from base import Problem


A = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
B = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
C = re.compile(r"Prize: X=(\d+), Y=(\d+)")


example = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""


def test_part1():
    p = D13(example)
    assert a_button((94, 34), (22, 67), (8400, 5400)) == 80
    assert b_button((94, 34), (22, 67), (8400, 5400)) == 40

    assert a_button((17, 86), (84, 37), (7870, 6450)) == 38
    assert b_button((17, 86), (84, 37), (7870, 6450)) == 86

    assert p.solve_p1() == 480


def test_part2():
    p = D13(example)
    assert p.solve_p2() == 875318608908


# Solve two equations system:
# -> X * ax + Y * bx = cx
# -> X * ay + Y * by = cy

# X = (bx * cy - by * cx) / (ay * bx - ax * by)
def a_button(a, b, c):

    ax, ay = a
    bx, by = b
    cx, cy = c

    return (bx * cy - by * cx) / (ay * bx - ax * by)


# Y = (ax * cy - ay * cx) / (by * ax - bx * ay)
def b_button(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c

    return (ax * cy - ay * cx) / (by * ax - bx * ay)


class D13(Problem):
    def solve_p1(self):
        n = 0
        for machine in self.data:
            a = a_button(*machine)
            b = b_button(*machine)
            if a.is_integer() and b.is_integer():
                n += a * 3 + b * 1
        return int(n)

    def solve_p2(self):
        offset = 10_000_000_000_000
        n = 0
        for machine in self.data:
            ma, mb, mc = machine
            mc = (mc[0] + offset, mc[1] + offset)
            a = a_button(ma, mb, mc)
            b = b_button(ma, mb, mc)
            if a.is_integer() and b.is_integer():
                n += a * 3 + b * 1
        return int(n)

    def parseinput(self, lines):
        data = []
        button = [(0, 0), (0, 0), (0, 0)]
        for i in lines:
            if not i.strip():
                continue
            matchA = A.match(i)
            matchB = B.match(i)
            matchC = C.match(i)
            if matchA:
                a = tuple(map(int, matchA.groups()))
                button[0] = a
            if matchB:
                b = tuple(map(int, matchB.groups()))
                button[1] = b
            if matchC:
                c = tuple(map(int, matchC.groups()))
                button[2] = c
                data.append(button)
                button = [(0, 0), (0, 0), (0, 0)]

        return data


if __name__ == "__main__":
    print("Day 13: Claw Contraption")

    p = D13("d13.data")
    print(p.solve_p1())
    print(p.solve_p2())
