from base import Problem
import operator
import itertools
from multiprocessing import Pool, cpu_count
from functools import lru_cache


example = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


@lru_cache
def concat(a, b):
    return int(f"{a}{b}")


OP1 = (operator.add, operator.mul)
OP2 = (operator.add, operator.mul, concat)


@lru_cache
def possible(test, eq, ops=OP1):
    n = len(eq) - 1
    ops = list(itertools.product(ops, repeat=n))

    for p in ops:
        x = eq[0]
        for i, o in enumerate(p):
            x = o(x, eq[i+1])
            if x > test:
                break
        if x == test:
            return True, test

    return False, test


def test_part1():
    p = D07(example)
    assert p.solve_p1() == 3749


def test_part2():
    p = D07(example)
    assert p.solve_p2() == 11387


class D07(Problem):
    def solve_p1(self):
        n = 0
        for k, *v in self.eqs:
            p, x = possible(k, tuple(v))
            if p:
                n += k
        return n

    def solve_p2(self):
        n = 0
        with Pool(cpu_count()) as p:
            res = p.starmap(possible, [(k, tuple(v), OP2) for k, *v in self.eqs])

        return sum(i for k, i in res if k)

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())

        self.eqs = []
        for line in data:
            t, rest = line.split(":")
            self.eqs.append((int(t), *(int(i) for i in rest.strip().split(" "))))

        return data


if __name__ == "__main__":
    print("Day 07: Bridge Repair")

    p = D07("d07.data")
    print(p.solve_p1())
    p = D07("d07.data")
    print(p.solve_p2())
