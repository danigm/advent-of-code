from base import Problem


example = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""


def test_part1():
    p = D16(example)
    assert len(p.data) == 10
    assert p.solve_p1() == 46


def test_part2():
    p = D16(example)
    assert p.solve_p2() == 51


class Top:
    @classmethod
    def next(cls, r, c):
        return r - 1, c

    @classmethod
    def beam(cls, tile):
        if tile == "-":
            return (Left, Right)
        if tile in "|.":
            return (Top, )
        if tile == "/":
            return (Right, )
        if tile == "\\":
            return (Left, )

class Bottom:
    @classmethod
    def next(cls, r, c):
        return r + 1, c

    @classmethod
    def beam(cls, tile):
        if tile == "-":
            return (Left, Right)
        if tile in "|.":
            return (Bottom, )
        if tile == "/":
            return (Left, )
        if tile == "\\":
            return (Right, )

class Left:
    @classmethod
    def next(cls, r, c):
        return r, c - 1

    @classmethod
    def beam(cls, tile):
        if tile in "-.":
            return (Left, )
        if tile == "|":
            return (Bottom, Top)
        if tile == "/":
            return (Bottom, )
        if tile == "\\":
            return (Top, )

class Right:
    @classmethod
    def next(cls, r, c):
        return r, c + 1

    @classmethod
    def beam(cls, tile):
        if tile in "-.":
            return (Right, )
        if tile == "|":
            return (Bottom, Top)
        if tile == "/":
            return (Top, )
        if tile == "\\":
            return (Bottom, )


class D16(Problem):
    def solve_p1(self, r=0, c=0, direction=Right):
        n = 0
        todo = set()
        todo.add((r, c, direction))
        while todo:
            r, c, direction = todo.pop()
            n1, ntodo = self.beam(r, c, direction)
            n += n1
            todo.update(ntodo)

        return n

    def solve_p2(self):
        max = 0
        nr = len(self.data)
        nc = len(self.data[0])
        for j in range(nc):
            # Top row
            self.reset()
            n = self.solve_p1(0, j, Bottom)
            max = n if n > max else max
            # Bottom row
            self.reset()
            n = self.solve_p1(nc - 1, j, Top)
            max = n if n > max else max

        for i in range(len(self.data)):
            # Left Column
            self.reset()
            n = self.solve_p1(i, 0, Right)
            max = n if n > max else max
            # Right Column
            self.reset()
            n = self.solve_p1(i, nr - 1, Left)
            max = n if n > max else max

        return max

    def reset(self):
        self.loops = {}
        self.energized = {}

    def beam(self, r=0, c=0, direction=Right):
        todo = set()
        if (r, c, direction) in self.loops:
            return 0, todo
        self.loops[(r, c, direction)] = True

        if r < 0 or c < 0 or r >= len(self.data) or c >= len(self.data[0]):
            return 0, todo

        tile = self.data[r][c]
        beams = direction.beam(tile)
        n = 1 if (r, c) not in self.energized else 0
        self.energized[(r, c)] = True
        for nd in beams:
            nr, nc = nd.next(r, c)
            todo.add((nr, nc, nd))

        return n, todo

    def parseinput(self, lines):
        self.loops = {}
        self.energized = {}
        data = tuple(tuple(i.strip()) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 16: The Floor Will Be Lava")

    p = D16("d16.data")
    print(p.solve_p1())
    print(p.solve_p2())
