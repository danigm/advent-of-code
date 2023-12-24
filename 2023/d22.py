from functools import lru_cache
from collections import defaultdict
from base import Problem


example = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


def test_part1():
    p = D22(example)
    s, l = p.settle()
    assert s[0].base == 1
    assert s[1].base == 2
    assert s[2].base == 2
    assert s[3].base == 3
    assert s[4].base == 3
    assert p.disintegrate(s) == 5
    p = D22(example)
    s, l = p.settle()
    assert p.solve_p1() == 5


def test_part2():
    p = D22(example)
    s, l = p.settle()
    assert p.chain_reaction(tuple(s), s[0]) == 6
    assert p.chain_reaction(tuple(s), s[-2]) == 1
    assert p.chain_reaction(tuple(s), s[1]) == 0
    assert p.chain_reaction(tuple(s), s[2]) == 0
    assert p.chain_reaction(tuple(s), s[3]) == 0
    assert p.solve_p2() == 7


class Cube(list):
    def __init__(self, x, y, z):
        super().__init__((x, y, z))
        self.x = x
        self.y = y
        self.z = z


class Brick:
    def __init__(self, start, end):
        self._start = Cube(*start)
        self._end = Cube(*end)

        dx, dy, dz = self.diff()
        self.direction = (dx and "x") or (dy and "y") or (dz or "z")
        if (dx, dy, dz) == (0, 0, 0):
            # one cube
            self.vector = 0
        else:
            self.vector = list(filter(None, self.diff()))[0]
        self.ncubes = abs(self.vector) + 1

        self.base = min(self._start[2], self._end[2])
        self.top = max(self.start[2], self.end[2])
        self._supported = None
        self._supporting = None

    def __repr__(self):
        return f"{self.start}~{self.end}"

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @start.setter
    def start(self, value):
        self._start = value
        self.base = min(self.start[2], self.end[2])
        self.top = max(self.start[2], self.end[2])

    @end.setter
    def end(self, value):
        self._end = value
        self.base = min(self.start[2], self.end[2])
        self.top = max(self.start[2], self.end[2])

    def supporting(self, bricks, exclude=None):
        if self._supporting is None:
            self._supporting = []
            for i in bricks:
                if i == self:
                    continue
                if self.top + 1 == i.base and self.collides(i):
                    self._supporting.append(i)
        if exclude is None:
            return self._supporting

        return list(filter(lambda x: x not in exclude, self._supporting))

    def supported(self, bricks, exclude=None):
        if self._supported is None:
            self._supported = []
            for i in bricks:
                if i == self:
                    continue
                if i.top + 1 == self.base and self.collides(i):
                    self._supported.append(i)

        if exclude is None:
            return self._supported

        return list(filter(lambda x: x not in exclude, self._supported))

    @lru_cache
    def collides(self, other):
        sx1, sy1, sz1 = self.start
        ex1, ey1, ez1 = self.end
        sx2, sy2, sz2 = other.start
        ex2, ey2, ez2 = other.end

        # just consider x, y
        collides_x = sx2 <= sx1 <= ex2 or sx1 <= sx2 <= ex1
        collides_y = sy2 <= sy1 <= ey2 or sy1 <= sy2 <= ey1

        return collides_x and collides_y

    def settle(self, to_z):
        diff_z = self.base - to_z

        x, y, z = self.start
        self.start = Cube(x, y, z - diff_z)
        x, y, z = self.end
        self.end = Cube(x, y, z - diff_z)

    def copy(self):
        return Brick(self.start, self.end)

    def diff(self):
        sx, sy, sz = self.start
        ex, ey, ez = self.end

        return ex - sx, ey - sy, ez - sz

    @classmethod
    def parse(cls, line):
        s, e = line.split("~")
        s = tuple((int(i) for i in s.split(",")))
        e = tuple((int(i) for i in e.split(",")))
        return cls(s, e)


class D22(Problem):
    def solve_p1(self):
        return self.disintegrate(self.s)

    def solve_p2(self):
        t = 0
        for b in self.s:
            t += self.chain_reaction(tuple(self.s), b)
        return t

    def settle(self):
        # start at Ground
        level = 0
        settled = [b.copy() for b in sorted(self.data, key=lambda b: b.base)]
        levels = defaultdict(list)

        prevs = []
        for brick in settled:
            if brick.base > level:
                level = level + 1
                brick.settle(level)
            for p in prevs:
                # if there's no collision with prev, go down
                level = p.base
                brick.settle(level)
                if brick.collides(p):
                    level = p.top + 1
                    brick.settle(level)
                    break
            levels[level].append(brick)
            prevs = sorted(prevs + [brick], key=lambda b: b.top, reverse=True)
            level = prevs[0].top

        self.s, self.l = settled, levels
        return settled, levels

    def disintegrate(self, bricks):
        total = set()
        for b in bricks:
            supporting = b.supporting(bricks)
            if not supporting:
                total.add(b)

            # check that all supporting bricks are supported by another brick
            all_supported = True
            for s in supporting:
                supported = s.supported(bricks, [s, b])
                all_supported = all_supported and bool(supported)
            if all_supported:
                total.add(b)

        return len(total)

    @lru_cache
    def chain_reaction(self, bricks, destroy):
        to_consider = destroy.supporting(bricks)
        destroyed = {destroy}

        prev = destroy
        while to_consider:
            new_step = []
            for i in to_consider:
                if not i.supported(bricks, destroyed | {i}):
                    destroyed.add(i)
                    new_step += i.supporting(bricks)
            to_consider = new_step

        return len(destroyed) - 1

    def parseinput(self, lines):
        lines = (l for l in lines if l.strip())
        bricks = []

        for i in lines:
            b = Brick.parse(i)
            bricks.append(b)

        return bricks


if __name__ == "__main__":
    print("Day 22: Sand Slabs")

    p = D22("d22.data")
    p.settle()
    print(p.solve_p1())
    print(p.solve_p2())
