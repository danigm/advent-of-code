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
# TODO: dictionary with distances from each key to all


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


def test_part1():
    assert seq(N, "A", "0") == set(("<",))
    assert seq(N, "0", "2") == set(("^",))
    assert seq(N, "2", "9") == set(("^>^", "^^>", ">^^"))
    assert seq(N, "9", "A") == set(("vvv", ))
    assert seq(N, "A", "1") == set(("<^<", "^<<"))
    assert seq(N, "4", "0") == set(("v>v", ">vv"))
    assert len(shortest_seq("029A", robots=1)) == 12
    assert len(shortest_seq("029A", robots=2)) == 28
    assert len(shortest_seq("029A", robots=3)) == 68
    assert len(shortest_seq("980A", robots=3)) == 60
    assert len(shortest_seq("179A", robots=3)) == 68
    assert len(shortest_seq("456A", robots=3)) == 64
    assert len(shortest_seq("379A", robots=3)) == 64

    p = D21(example)
    assert p.solve_p1() == 126384


def test_part2():
    p = D21(example)
    assert p.solve_p2() == 0


def shortest_seq(sequence, robots=1):
    if robots == 1:
        pad = N
        ss = sequence
    else:
        pad = R
        ss = shortest_seq(sequence, robots=robots - 1)

    r = []
    pos = "A"
    for s in ss:
        # TODO: evaluate all to get the shortest
        x = seq(pad, pos, s)
        pos = s
        r.append(x + "A")
        
    s = "".join(r)
    return s


class D21(Problem):
    def solve_p1(self):
        # Lenght of shortest sequence * numeric part of the code
        r = 3
        s = 0
        for i in self.data:
            x = shortest_seq(i, r)
            s += len(x) * int(i[:-1])
        return s

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 21: Keypad Conundrum")

    p = D21("d21.data")
    print(p.solve_p1())
    print(p.solve_p2())
