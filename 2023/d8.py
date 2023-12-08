import math
from base import Problem


example = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""


example2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


example3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def test_d8_part2():
    p = D8(example3)
    assert p.solve_p2() == 6


def test_d8_part1():
    p = D8(example)

    assert p.instructions == "RL"
    assert p.btree["AAA"] == (("BBB", "CCC"))
    assert len(p.btree) == 7
    assert p.steps() == 2
    assert p.solve_p1() == 2

    p = D8(example2)
    assert p.solve_p1() == 6


class D8(Problem):
    def solve_p1(self):
        return self.steps()

    def solve_p2(self):
        nodes = [n for n in self.btree if n.endswith("A")]

        # calc the number of steps for each node to get to a end and the
        # combined end is the "least common multiple", because we should follow
        # the instructions until all are at the end, and that requires iterate
        # over the instructions "lcm" times.
        mins = [self.steps(n, "Z", endswith=True) for n in nodes]
        return math.lcm(*mins)

    def parseinput(self, lines):
        data = super().parseinput(lines)

        self.instructions = data[0]
        self.btree = {}

        for line in data[1:]:
            node, rest = line.split("=")
            node = node.strip()
            left, right = rest.strip().split(",")
            left = left.strip()[1:]
            right = right.strip()[:-1]
            self.btree[node] = ((left, right))

        return data

    def steps(self, src="AAA", dst="ZZZ", endswith=False):
        node = src
        i = 0

        def condition():
            if endswith:
                return node.endswith(dst)
            return node == dst

        while not condition():
            direction = self.dir(i)
            options = self.btree[node]
            node = options[direction]
            i += 1

        return i

    def dir(self, n=0):
        lr = self.instructions[n % len(self.instructions)]
        return "LR".index(lr)


if __name__ == "__main__":
    print("Day 8: Haunted Wasteland")

    p = D8("d8.data")
    print(p.solve_p1())
    print(p.solve_p2())
