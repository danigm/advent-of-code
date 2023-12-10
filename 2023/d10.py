import itertools
from enum import Enum
from base import Problem


example = """
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""


example2 = """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""


example3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""


example4 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


example5 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def test_part1():
    p = D10(example)
    p1 = D10(example2)

    assert p.tiles[(1,1)].tile == "S"
    assert p.tiles[(1,1)].starting
    assert p.tiles[(1,0)].tile == "L"
    c1, c2 = p.tiles[(1,0)].connections()
    assert c1 == (1,-1)
    assert p.tiles.get(c1) is None
    assert p.tiles[c2].tile == "|"
    x = p.tiles[(2,1)]
    assert x.next(1, 1) == (3, 1)
    assert x.next(3, 1) == (1, 1)

    assert p.starting == (1, 1)
    assert p1.starting == (0, 2)
    assert p.tiles[p.starting].tile == "S"
    assert p1.tiles[p1.starting].tile == "S"

    assert p.solve_p1() == 4
    assert p1.solve_p1() == 8


def test_part2():
    p01 = D10(example)
    p02 = D10(example2)
    p1 = D10(example3)
    p2 = D10(example4)
    p3 = D10(example5)

    p01.find_start_loop()
    assert p01.loop.area(p01.tiles) == 1
    p02.find_start_loop()
    assert p02.loop.area(p02.tiles) == 1

    p1.find_start_loop()
    assert p1.loop.area(p1.tiles) == 4
    p2.find_start_loop()
    assert p2.loop.area(p2.tiles) == 8
    p3.find_start_loop()
    assert p3.loop.area(p3.tiles) == 10


class TileType(Enum):
    Ground = 1
    Vertical = 2
    Horizontal = 3
    NorthEast = 4
    NorthWest = 5
    SouthWest = 6
    SouthEast = 7


TILES = {
    ".": TileType.Ground,
    "|": TileType.Vertical,
    "-": TileType.Horizontal,
    "L": TileType.NorthEast,
    "J": TileType.NorthWest,
    "7": TileType.SouthWest,
    "F": TileType.SouthEast,
}


class Tile:
    def __init__(self, x, y, letter="."):
        self.x = x
        self.y = y
        self.tile = letter
        self.starting = letter == "S"
        self.type = None
        if not self.starting:
            self.type = TILES[letter]

    def __repr__(self):
        return f"{self.tile} ({self.x},{self.y})"

    def is_rect(self):
        return self.type in [TileType.Vertical, TileType.Horizontal]

    def from_north(self):
        return self.type in [TileType.NorthEast, TileType.NorthWest]

    def connections(self):
        match self.type:
            case TileType.Vertical:
                return ((self.x, self.y - 1), (self.x, self.y + 1))
            case TileType.Horizontal:
                return ((self.x - 1, self.y), (self.x + 1, self.y))
            case TileType.NorthEast:
                return ((self.x, self.y - 1), (self.x + 1, self.y))
            case TileType.NorthWest:
                return ((self.x, self.y - 1), (self.x - 1, self.y))
            case TileType.SouthWest:
                return ((self.x, self.y + 1), (self.x - 1, self.y))
            case TileType.SouthEast:
                return ((self.x, self.y + 1), (self.x + 1, self.y))
        return (None, None)

    def next(self, sx, sy):
        conns = self.connections()
        match self.type:
            case TileType.Vertical:
                return conns[1] if sy < self.y else conns[0]
            case TileType.Horizontal:
                return conns[1] if sx < self.x else conns[0]
            case TileType.NorthEast | TileType.NorthWest:
                return conns[1] if sy < self.y else conns[0]
            case TileType.SouthWest | TileType.SouthEast:
                return conns[1] if sy > self.y else conns[0]

        return None


class Loop:
    def __init__(self, points=None):
        if points is None:
            points = []
        self.points = points
        self.pm = {}
        for p in self.points:
            self.pm[(p.x, p.y)] = p

    def add(self, point):
        self.points.append(point)
        self.pm[(point.x, point.y)] = p

    def _area_lines(self):
        # Remove the rect lines, that points are not relevant for the
        # area calculation, we just need vertices
        points = [i for i in self.points if not i.is_rect()]
        points = sorted(points, key=lambda t: (t.y, t.x))
        # group lines by "y"
        lines = itertools.groupby(points, key=lambda t: t.y)
        lines = [list(g) for k, g in lines]
        return lines

    def area(self, tiles):
        """
        Split the polygon in rectangles

        * Go top to bottom
        * Get all the points with minimum y
        * Find the next first point that y' > y
        * Extend points to bottom and calc each rectangle area:
            - (x0,y,x1,y')
            - (x2,y,x3,y')
            - ...
            - (xN,y,xN1,y')
        * Move to bottom and do the same again:
            - Copy points that doesn't exists, if (xN,y') == "|", add
              to the list.
            - Remove points that doesn't add anything, if (xN,y') in
              ["L", "J"], remove the point from the list.
        """

        lines = self._area_lines()
        area = 0
        cl = lines.pop(0)
        while lines:
            next = lines.pop(0)
            ny = next[0].y
            for i in range(0, len(cl), 2):
                v1 = cl[i]
                v2 = cl[i+1]
                area += (v2.x - v1.x - 1) * (ny - v1.y - 1)

                v3 = tiles[(v1.x, ny)]
                v4 = tiles[(v2.x, ny)]
                self._handle_point(v3, next)
                self._handle_point(v4, next)
                area += self._handle_inner(v1, v2, ny, tiles)

            cl = sorted(next, key=lambda t: t.x)

        return area

    def _handle_inner(self, v1, v2, ny, tiles):
        # Add all inner points
        area = 0
        for j in range(v1.x + 1, v2.x):
            t = (j, ny)
            if t not in self.pm:
                area += 1
        return area

    def _handle_point(self, p, next):
        # Add vertical nodes for the next round
        # Remove the L and J nodes for the next round
        if p.type == TileType.Vertical:
            next.append(p)
        elif p.from_north():
            next.remove(p)

    def __repr__(self):
        return f"{self.points}"


class D10(Problem):
    def solve_p1(self):
        return self.find_start_loop()

    def solve_p2(self):
        return self.loop.area(self.tiles)

    def find_start_loop(self):
        sx, sy = self.starting
        conns = self.start_connections()
        c = conns[0]
        return self.loop_steps(c.x, c.y, sx, sy)

    def loop_steps(self, x, y, sx, sy):
        """
        Iterative calculation of the furthest tile
        """
        tile = self.tiles.get((x, y))
        self.loop.add(tile)
        steps = 1
        while not tile.starting:
            steps += 1
            n = tile.next(sx, sy)
            if not n:
                return None
            x1, y1 = n
            sx, sy = tile.x, tile.y
            tile = self.tiles.get((x1, y1))
            self.loop.add(tile)

        return steps // 2

    def find_loop(self, x, y, sx=None, sy=None, step=0):
        # The recursive loop is not valid, too deep, maximum deep recursion
        tile = self.tiles.get((x, y))
        if tile.tile == "S":
            return [(x, y, step)]

        n = tile.next(sx, sy)
        # Dead end
        if not n:
            return [(x, y, step), None]

        x1, y1 = n
        return [(x, y, step)] + self.find_loop(x1, y1, sx=x, sy=y, step=step + 1)

    def start_connections(self):
        s = self.tiles[self.starting]
        north = self.tiles.get((s.x, s.y - 1))
        south = self.tiles.get((s.x, s.y + 1))
        west = self.tiles.get((s.x - 1, s.y))
        east = self.tiles.get((s.x + 1, s.y))

        connections = []
        if north and self.starting in north.connections():
            connections.append(north)
        if south and self.starting in south.connections():
            connections.append(south)
        if west and self.starting in west.connections():
            connections.append(west)
        if east and self.starting in east.connections():
            connections.append(east)

        return connections

    def parseinput(self, lines):
        data = super().parseinput(lines)

        self.tiles = {}
        self.starting = (0, 0)
        self.loop = Loop()
        for y, line in enumerate(data):
            for x, t in enumerate(line):
                if t == "S":
                    self.starting = (x, y)
                self.tiles[(x, y)] = Tile(x, y, t)

        return data


if __name__ == "__main__":
    print("Day 10: Pipe Maze")

    p = D10("d10.data")
    print(p.solve_p1())
    print(p.solve_p2())
