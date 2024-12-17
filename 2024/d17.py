import re
import itertools
from collections import defaultdict
import heapq
from base import Problem


R = re.compile(r"Register (A|B|C): (\d+)")
P = re.compile(r"Program: ([\d,]+)")


example = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


example2 = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""


class Device:
    def __init__(self, check=False):
        self.INS = 0
        self.OUT = []
        self.REGS = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        self.COMBO = [0, 1, 2, 3, "A", "B", "C"]
        self.OPCODE = [self.adv, self.bxl, self.bst, self.jnz,
                       self.bxc, self.out, self.bdv, self.cdv]

        self.check = check
        self.program = []
        self.ERR = None

    def run(self, p, a, b, c):
        self.REGS["A"] = a
        self.REGS["B"] = b
        self.REGS["C"] = c
        self.program = p

        self.INS = 0
        self.OUT = []
        while self.INS < len(p):
            if self.INS == 0:
                a = self.REGS["A"]
            op = self.OPCODE[p[self.INS]]
            operand = p[self.INS + 1]
            r = op(operand)

            if op == self.jnz and r:
                continue

            self.INS += 2

        return tuple(self.OUT)

    def combo(self, operand):
        c = self.COMBO[operand]
        if c in self.REGS:
            c = self.REGS[c]
        return c

    def literal(self, operand):
        return operand

    def adv(self, operand):
        d = 2 ** self.combo(operand)
        self.REGS["A"] = self.REGS["A"] // d

    def bxl(self, operand):
        c = self.literal(operand)
        self.REGS["B"] = self.REGS["B"] ^ operand

    def bst(self, operand):
        c = self.combo(operand)
        self.REGS["B"] = c % 8

    def jnz(self, operand):
        if self.REGS["A"] == 0:
            return False
        c = self.literal(operand)
        self.INS = c
        return True

    def bxc(self, operand):
        c = self.literal(operand)
        self.REGS["B"] = self.REGS["B"] ^ self.REGS["C"]

    def out(self, operand):
        c = self.combo(operand)
        v = c % 8
        self.OUT.append(v)
        if self.check and self.program[len(self.OUT) - 1] != v:
            self.ERR = self.OUT
            raise Exception

    def bdv(self, operand):
        d = 2 ** self.combo(operand)
        self.REGS["B"] = self.REGS["A"] // d

    def cdv(self, operand):
        d = 2 ** self.combo(operand)
        self.REGS["C"] = self.REGS["A"] // d


def test_part1():
    p = D17(example)
    assert p.solve_p1() == "4,6,3,5,6,3,5,2,1,0"


def test_part2():
    p = D17(example2)
    assert p.solve_p2() == 117440


class D17(Problem):
    def solve_p1(self):
        p, r = self.data
        d = Device()
        d.run(p, r["A"], r["B"], r["C"])
        out = ",".join(str(i) for i in d.OUT)
        return out

    def solve_p2(self):
        """
        DFS algorithm to find the number compound of binaries of 3
        digits.

        The last number in the program should be the output for the
        run with A = X = xxx(binary).
        The last two numbers in the program should be the output for
        the run with A = xxx yyy (binary)
        The last three numbers in the program should be the output for
        the run with A = xxx yyy zzz (binary)
        ...
        """

        d = Device(check=False)
        p, r = self.data

        s = None
        visited = set()
        queue = list(range(8))
        while queue:
            a = heapq.heappop(queue)
            visited.add(a)
            out = d.run(p, a, 0, 0)
            if out == p:
                s  = a
                break

            if out == p[-len(out):]:
                # possible solution
                for i in range(8):
                    n = int(f"{a:b}{i:03b}", 2)
                    if n in visited:
                        continue
                    heapq.heappush(queue, n)

        return s

    def parseinput(self, lines):
        p = []
        regs = {"A": 0, "B": 0, "C": 0}
        for line in lines:
            ma = R.match(line)
            mp = P.match(line)
            if ma:
                r, v = ma.groups()
                regs[r] = int(v)
            if mp:
                p = list(map(int, mp.group(1).split(",")))
        return tuple(p), regs


if __name__ == "__main__":
    print("Day 17: Chronospatial Computer")

    p = D17("d17.data")
    print(p.solve_p1())
    print(p.solve_p2())
