import math
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

example3 = """
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""


def test_part1():
    p = D15(example2)
    assert p.solve_p1() == 2028
    p = D15(example)
    assert p.solve_p1() == 10092


def test_part2():
    p = D15(example)
    assert p.solve_p2() == 9021


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


@lru_cache(maxsize=None)
def move_box(box, state, w, h, movement):
    bi, bj = box
    mi, mj = M[movement]

    c = ch(state, w, bi, bj)
    if c == ".":
        return True, state

    if c == "[":
        b1i, b1j = box
        b2i, b2j = b1i, b1j + 1
    else:
        b2i, b2j = box
        b1i, b1j = b2i, b2j - 1

    n1i, n1j = b1i + mi, b1j + mj
    n2i, n2j = b2i + mi, b2j + mj

    c1 = ch(state, w, b1i, b1j)
    c2 = ch(state, w, b2i, b2j)
    if c1 == "#":
        return False, state

    if c1 in "[]":
        old_state = state
        ok1, ok2 = False, False
        ok1, state = move_box((n1i, n1j), state, w, h, movement)
        if ok1:
            ok2, state = move_box((n2i, n2j), state, w, h, movement)
            if ok2:
                st = list(state)
                chv(st, w, n1i, n1j, "[")
                chv(st, w, n2i, n2j, "]")
                chv(st, w, b1i, b1j, ".")
                chv(st, w, b2i, b2j, ".")
                state = "".join(st)
            else:
                state = old_state
        else:
            state = old_state
        return ok1 and ok2, state

    if c1 == "." and c2 == ".":
        return True, state

    return False, state


@lru_cache(maxsize=None)
def move2(robot, state, w, h, movement):
    ri, rj = robot
    mi, mj = M[movement]
    ni, nj = ri + mi, rj + mj

    c = ch(state, w, ni, nj)

    if c == "#":
        # can't move
        return robot, state

    if c == ".":
        robot = ni, nj
        st = list(state)
        chv(st, w, ri, rj, ".")
        chv(st, w, ni, nj, "@")
        state = "".join(st)

    # Left and right
    if c in "[]" and movement in "<>":
        ei, ej = ni + mi, nj + mj
        ei2, ej2 = ei + mi, ej + mj
        n = 1
        # find empty space
        while True:
            c = ch(state, w, ei, ej)
            if c == "#":
                return robot, state
            if c == ".":
                st = list(state)
                chv(st, w, ei, ej, "[" if movement == "<" else "]")
                for j in range(n):
                    j = nj + (mj * j)
                    c = ch(state, w, ni, j)
                    chv(st, w, ni, j, "]" if c == "[" else "[")
                chv(st, w, ri, rj, ".")
                chv(st, w, ni, nj, "@")
                robot = ni, nj
                state = "".join(st)
                break
            ei, ej = ei + mi, ej + mj
            ei2, ej2 = ei + mi, ej + mj
            n += 1

    # Up and down
    if c in "[]" and movement in "^v":
        ok, state = move_box((ni, nj), state, w, h, movement)
        if ok:
            st = list(state)
            chv(st, w, ri, rj, ".")
            chv(st, w, ni, nj, "@")
            robot = ni, nj
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


def sum(state, w, h, box="O"):
    """
    100 * i + j
    """

    s = 0
    for i in range(h):
        for j in range(w):
            if ch(state, w, i, j) == box:
                s += 100 * i + j
    return s


class D15(Problem):
    def solve_p1(self):
        r, s = self.robot, self.initial
        for m in self.moves:
            r, s = move(r, s, self.w, self.h, m)

        return sum(s, self.w, self.h)

    def solve_p2(self):
        w, h = self.w * 2, self.h
        ri, rj = self.robot

        r = ri, rj * 2
        s = self.expanded

        for m in self.moves:
            r, s = move2(r, s, w, h, m)

        return sum(s, w, h, "[")

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
        self.expanded = self.initial.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
        return data


if __name__ == "__main__":
    print("Day 15: Warehouse Woes")

    p = D15("d15.data")
    print(p.solve_p1())
    print(p.solve_p2())
