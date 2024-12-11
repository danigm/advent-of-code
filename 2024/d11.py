from base import Problem
from functools import lru_cache


example = """
0 1 10 99 999
"""

example2 = """
125 17
"""


def test_part2():
    p = D11(example)
    assert p.solve_p2(1) == 7
    p = D11(example2)
    assert p.solve_p2(25) == 55312


class D11(Problem):
    @lru_cache(maxsize=None)
    def stone_blink(self, n):
        c = str(n)
        if n == 0:
            return (1, )
        elif len(c) % 2 == 0:
            half = len(c) // 2
            a, b = c[:half], c[half:]
            return int(a), int(b)
        return (n * 2024, )

    @lru_cache(maxsize=None)
    def rsolve(self, blinks, stone):
        n = 0
        if blinks == 0:
            return 1

        state = self.stone_blink(stone)
        for ns in state:
            n += self.rsolve(blinks - 1, ns)

        return n

    def solve_p2(self, blinks=25):
        return sum(self.rsolve(blinks, i) for i in self.data)


    def parseinput(self, lines):
        data = tuple(tuple(int(j) for j in i.strip().split()) for i in lines if i.strip())
        return data[0]


if __name__ == "__main__":
    print("Day 11: Plutonian Pebbles")

    p = D11("d11.data")
    print(p.solve_p2(25))
    p = D11("d11.data")
    print(p.solve_p2(75))
