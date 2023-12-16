from base import Problem


example = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def test_part1():
    p = D15(example)
    assert hash("HASH") == 52
    assert hash("rn=1") == 30
    assert p.solve_p1() == 1320


def test_part2():
    p = D15(example)
    assert p.solve_p2() == 0


def hash(line):
    v = 0
    for i in line:
        n = ord(i)
        v = ((v + n) * 17) % 256

    return v


class D15(Problem):
    def solve_p1(self):
        return sum(hash(i) for i in self.data)

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        lines = super().parseinput(lines)
        data = lines[0].strip()
        data = data.split(",")
        return data


if __name__ == "__main__":
    print("Day 15: ")

    p = D15("d15.data")
    print(p.solve_p1())
    print(p.solve_p2())
