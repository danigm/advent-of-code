import re
from functools import lru_cache
from collections import defaultdict
from base import Problem


R = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")


example = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def table(npos, w, h):
    print(f"{w} x {h}")
    for y in range(0, h):
        for x in range(0, w):
            n = npos[(x, y)]
            print(n if n else ".", end="")
        print("\n", end="")


lru_cache(maxsize=None)
def move(px, py, vx, vy, seconds=1, w=11, h=7):
    x = (px + vx * seconds) % w
    y = (py + vy * seconds) % h
    return x, y


def test_part1():
    p = D14(example)
    assert move(2, 4, 2, -3, seconds=5, w=11, h=7) == (1, 3)
    assert p.solve_p1(w=11, h=7) == 12


def test_part2():
    p = D14(example)
    assert p.solve_p2() == 0


class D14(Problem):
    def solve_p1(self, w=101, h=103):
        npos = defaultdict(int)
        for r in self.data:
            p = move(*r, seconds=100, w=w, h=h)
            npos[p] += 1

        # each quadrant
        q1, q2, q3, q4 = 0, 0, 0, 0
        w2 = w // 2
        h2 = h // 2
        for x in range(0, w):
            for y in range(0, h):
                if x < w2:
                    if y < h2:
                        q1 += npos[(x, y)]
                    elif y > h2:
                        q3 += npos[(x, y)]
                elif x > w2:
                    if y < h2:
                        q2 += npos[(x, y)]
                    elif y > h2:
                        q4 += npos[(x, y)]

        return q1 * q2 * q3 * q4

    def solve_p2(self):
        w = 101
        h = 103
        seconds = 0
        while True:
            seconds += 1
            npos = defaultdict(int)
            rows = defaultdict(int)
            for r in self.data:
                p = move(*r, seconds=seconds, w=w, h=h)
                rows[p[1]] += 1
                npos[p] += 1

                # Not unique
                if npos[p] > 1:
                    break

            m = max(n for n in rows.values())
            if m > 15:
                print(f"SECONDS: {seconds}")
                table(npos, w, h)
                break

        return seconds

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        robots = set()
        for line in data:
            r = tuple(map(int, R.match(line).groups()))
            robots.add(r)
        return robots


if __name__ == "__main__":
    print("Day 14: Restroom Redoubt")

    p = D14("d14.data")
    print(p.solve_p1())
    print(p.solve_p2())
