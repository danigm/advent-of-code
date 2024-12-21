"""
Help from:
https://github.com/mkern75/AdventOfCodePython/blob/main/year2024/Day21.py

I was unable to solve this one, check for solutions and I found this one that's
pretty similar to what I was doing.

The key point that I was missing was the recursion that I was doing in a
different way.

The key point to solve this is to solve the same problem for each subset of
keys in a lower level, for example:
    * (<v<A, <<vA, v<<A)
"""


from itertools import permutations
from functools import cache
from base import Problem


N = (
    "789",
    "456",
    "123",
    "-0A",
)
R = (
    "-^A",
    "<v>",
)


example = """
029A
980A
179A
456A
379A
"""


M = {
    "^": ( 0, -1),
    "v": ( 0,  1),
    "<": (-1,  0),
    ">": ( 1,  0),
}


@cache
def valid(pad, src, moves):
    sx, sy = src
    for m in moves:
        mx, my = M[m]
        sx, sy = sx + mx, sy + my
        if pad[sy][sx] == "-":
            return False
    return True


@cache
def seq(pad, src, dst):
    for y, line in enumerate(pad):
        for x, c in enumerate(line):
            if c == src:
                sx, sy = (x, y)
            if c == dst:
                dx, dy = (x, y)
    fx = dx - sx
    fy = dy - sy

    mx, my = 1, 1
    if fx < 0:
        x = "<" * -fx
        mx = -1
    else:
        x = ">" * fx
    if fy < 0:
        y = "^" * -fy
        my = -1
    else:
        y = "v" * fy

    p = tuple("".join(i) for i in permutations(y + x))
    return set(i for i in p if valid(pad, (sx, sy), i))


def all_paths(sequence, pad):
    r = []
    pos = "A"
    for s in sequence:
        seqs = seq(pad, pos, s)
        pos = s
        r.append([x + "A" for x in seqs])
    return r


@cache
def shortest_seq(sequence, robots=1, pad=N):
    if robots == 0:
        return len(sequence)

    res = 0
    for paths in all_paths(sequence, pad):
        res += min(shortest_seq(sp, robots - 1, R) for sp in paths)

    return res


def test_part1():
    assert seq(N, "A", "0") == set(("<",))
    assert seq(N, "0", "2") == set(("^",))
    assert seq(N, "2", "9") == set(("^>^", "^^>", ">^^"))
    assert seq(N, "9", "A") == set(("vvv", ))
    assert seq(N, "A", "1") == set(("<^<", "^<<"))
    assert seq(N, "4", "0") == set(("v>v", ">vv"))
    assert shortest_seq("029A", 1) == 12
    assert shortest_seq("029A", 2) == 28
    assert shortest_seq("029A", 3) == 68
    assert shortest_seq("980A", 3) == 60
    assert shortest_seq("179A", 3) == 68
    assert shortest_seq("456A", 3) == 64
    assert shortest_seq("379A", 3) == 64

    p = D21(example)
    assert p.solve_p1() == 126384


def test_part2():
    p = D21(example)
    assert p.solve_p2() == 154115708116294


class D21(Problem):
    def solve_p1(self):
        # Lenght of shortest sequence * numeric part of the code
        r = 3
        s = 0
        for i in self.data:
            x = shortest_seq(i, r)
            s += x * int(i[:-1])
        return s

    def solve_p2(self):
        # Lenght of shortest sequence * numeric part of the code
        r = 26
        s = 0
        for i in self.data:
            x = shortest_seq(i, r)
            s += x * int(i[:-1])
        return s

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 21: Keypad Conundrum")

    p = D21("d21.data")
    print(p.solve_p1())
    print(p.solve_p2())
