from base import Problem


example = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


def test_part1():
    p = D24(example)
    # print(p.intersect(p.hails[0], p.hails[1]))
    assert p.solve_p1() == 2


def test_part2():
    p = D24(example)
    assert p.solve_p2() == 0


class D24(Problem):
    def solve_p1(self, t1=7, t2=27):
        count = 0
        for i, h1 in enumerate(self.hails):
            for h2 in self.hails[i+1:]:
                intersection = self.intersect(h1, h2)
                if intersection is None:
                    continue
                px, py = intersection
                if t1 <= px <= t2 and t1 <= py <= t2:
                    count += 1
        return count

    def solve_p2(self):
        return 0

    # https://en.m.wikipedia.org/wiki/Line%E2%80%93line_intersection
    def intersect(self, h1, h2):
        p1, v1 = h1
        p2, v2 = h2

        x1, y1, z1 = p1
        x2, y2, z2 = x1 + v1[0], y1 + v1[1], z1 + v1[2]

        x3, y3, z3 = p2
        x4, y4, z4 = x3 + v2[0], y3 + v2[1], z3 + v2[2]

        px = (x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)
        dn1 = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if dn1 == 0:
            return None
        px = px / dn1

        py = (x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)
        dn2 = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
        if dn2 == 0:
            return None
        py = py / dn2

        # intersection in the past
        if px < x1 and v1[0] > 0:
            return None
        if px > x1 and v1[0] < 0:
            return None

        if px > x3 and v2[0] < 0:
            return None
        if px < x3 and v2[0] > 0:
            return None

        if py < y1 and v1[1] > 0:
            return None
        if py > y1 and v1[1] < 0:
            return None

        if py < y3 and v2[1] > 0:
            return None
        if py > y3 and v2[1] < 0:
            return None

        return px, py

    def parseinput(self, lines):
        data = tuple(i for i in lines if i.strip())

        hails = []
        for line in data:
            pos, vel = line.split("@")
            pos = [int(i) for i in pos.split(",")]
            vel = [int(i) for i in vel.split(",")]
            hails.append((pos, vel))
        self.hails = hails

        return data


if __name__ == "__main__":
    print("Day 24: Never Tell Me The Odds")

    p = D24("d24.data")
    print(p.solve_p1(200000000000000, 400000000000000))
    print(p.solve_p2())
