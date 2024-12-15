from functools import lru_cache
from base import Problem


example = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

example2 = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""


def test_part1():
    p = D15(example2)
    assert p.solve_p1() == 2028
    p = D15(example)
    assert p.solve_p1() == 10092


def test_part2():
    p = D15(example)
    assert p.solve_p2() == 0


M = {
    "^": (-1, 0),   
    "v": (1, 0),   
    "<": (0, -1),   
    ">": (0, 1),   
}


@lru_cache(maxsize=None)
def move(robot, state, w, h, movement):
    ri, rj = robot
    mi, mj = M[movement]
    ni, nj = ri + mi, rj + mj

    if ni < 0 or ni > h:
        return robot, state
    if nj < 0 or nj > w:
        return robot, state

    c = ch(state, w, ni, nj)

    if c == "#":
        # can't move
        return robot, state

    if c == "O":
        ei, ej = ni + mi, nj + mj
        # find empty space
        while True:
            c = ch(state, w, ei, ej)
            if c == "#":
                return robot, state
            if c == ".":
                st = list(state)
                chv(st, w, ei, ej, "O")
                chv(st, w, ri, rj, ".")
                chv(st, w, ni, nj, "@")
                robot = ni, nj
                state = "".join(st)
                break
            ei, ej = ei + mi, ej + mj

    if c == ".":
        robot = ni, nj
        st = list(state)
        chv(st, w, ri, rj, ".")
        chv(st, w, ni, nj, "@")
        state = "".join(st)

    return robot, state


def ch(state, w, i, j):
    return state[(i * w) + j]


def chv(state, w, i, j, v):
    state[(i * w) + j] = v


def pstate(state, w, h):
    for i in range(h):
        for j in range(w):
            print(ch(state, w, i, j), end="")
        print("\n", end="")


def sum(state, w, h):
    """
    100 * i + j
    """

    s = 0
    for i in range(h):
        for j in range(w):
            if ch(state, w, i, j) == "O":
                s += 100 * i + j
    return s


class D15(Problem):
    def sum(self):
        """
        100 * i + j
        """
        return sum(100 * bi + bj for bi, bj in self.boxes)

    def solve_p1(self):
        r, s = self.robot, self.initial
        for m in self.moves:
            r, s = move(r, s, self.w, self.h, m)

        return sum(s, self.w, self.h)

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        self.robot = (0, 0)
        self.boxes = set()
        self.walls = set()
        self.moves = []
        self.w = 0
        self.h = 0

        data = ""
        state = False

        ioffset = 0
        for i, l in enumerate(lines):
            l = l.strip()
            if not l:
                if data:
                    state = True
                    self.h = int(len(data) / self.w)
                ioffset += 1
                continue

            if not state:
                self.w = len(l)
                data += l

            for j, c in enumerate(l):
                if c == "#":
                    self.walls.add((i - ioffset, j))
                elif c == "O":
                    self.boxes.add((i - ioffset, j))
                elif c == "@":
                    self.robot = (i - ioffset, j)
                elif c == ".":
                    continue
                else:
                    self.moves.append(c)

        self.initial = data
        return data


if __name__ == "__main__":
    print("Day 15: Warehouse Woes")

    p = D15("d15.data")
    print(p.solve_p1())
    print(p.solve_p2())
