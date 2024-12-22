from collections import deque, defaultdict
from base import Problem


example = """
1
10
100
2024
"""


example2 = """
1
2
3
2024
"""


def secret(n, reps=1, best=None):
    initial = n
    seq = deque(maxlen=4)
    prev = n
    pn = int(str(prev)[-1])

    visited = set()
    while reps:
        n = ((n * 64) ^ n) % 16777216
        n = ((n // 32) ^ n) % 16777216
        n = ((n * 2048) ^ n) % 16777216
        reps -= 1

        nn = int(str(n)[-1])
        seq.append(nn - pn)

        prev = n
        pn = nn

        k = tuple(seq)
        if len(seq) == 4 and best is not None and k not in visited:
            best[k] += nn
            visited.add(k)

    return n


def test_part1():
    p = D22(example)
    assert secret(123, 1) == 15887950
    assert secret(15887950, 1) == 16495136
    assert secret(123, 2) == 16495136

    assert secret(1, 2000) == 8685429
    assert secret(10, 2000) == 4700978
    assert secret(100, 2000) == 15273692
    assert secret(2024, 2000) == 8667524
    assert p.solve_p1() == 37327623


def test_part2():
    p = D22(example2)
    best = defaultdict(int)
    assert secret(123, 9, best) == 7753432
    assert p.solve_p2() == 23


class D22(Problem):
    def solve_p1(self):
        return sum(secret(i, 2000) for i in self.data)

    def solve_p2(self):
        best = defaultdict(int)
        for i in self.data:
            secret(i, 2000, best)
        return max(i for i in best.values())

    def parseinput(self, lines):
        data = tuple(int(i.strip()) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 22: Monkey Market")

    p = D22("d22.data")
    print(p.solve_p1())
    print(p.solve_p2())
