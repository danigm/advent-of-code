from base import Problem


H = 0
V = 1


example = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


example2 = """
.....####..
##...####.#
##..#....#.
.....####..
####.####.#
##..#.##.#.
##.###..###
...#......#
..#.######.
##.##.##.##
..#..#..#..
##.#.####.#
####..##..#

#..##...#.####.##
#..##...#.####.##
....###.#..#.###.
#####..####..#.##
#..#..##...###..#
.##.##..#..###...
.##.#.#.#...#..#.
##.#...#.#.....#.
........######.#.
....#..#....#..##
#######..#.##..#.
#..#...#######..#
....###..###.##.#
"""


def test_part1():
    p = D13(example)
    assert len(p.patterns) == 2
    p0, p1 = p.patterns
    assert p0.rows[0] == "#.##..##."
    assert p0.rows[-1] == "#.#.##.#."
    assert p0.columns[0] == "#.##..#"
    assert p0.columns[-1] == "..##..."
    assert p0.reflection(H) == 0
    assert p0.reflection(V) == 5

    assert p1.rows[0] == "#...##..#"
    assert p1.rows[-1] == "#....#..#"
    assert p1.columns[0] == "##.##.#"
    assert p1.columns[-1] == "###..##"
    assert p1.reflection(V) == 0
    assert p1.reflection(H) == 4

    assert p.solve_p1() == 405


def test_part2():
    p = D13(example)
    p0, p1 = p.patterns
    assert p0.fix_smudge((5, V)) == (300, (0, 0))
    assert p1.fix_smudge((4, H)) == (100, (0, 4))
    assert p.solve_p2() == 400


def test_bug():
    p = D13(example2)
    p0, p1 = p.patterns
    assert p0.reflection(V) == 1
    assert p0.fix_smudge((1, V)) == (7, (1, 3))
    assert p1.reflection(H) == 1
    assert p1.fix_smudge((1, H)) == (2, (7, 1))


class Pattern:
    def __init__(self, input):
        self.rows = input
        self.columns = []
        # Store columns as rows so we can do the reflection the same way for
        # both directions
        for i in range(len(self.rows[0])):
            c = [n[i] for n in self.rows]
            self.columns.append("".join(c))

    def reflection(self, direction=H):
        data = self.rows
        if direction == V:
            data = self.columns

        return self._ref(data)

    def _ref(self, data, ignore=None):
        n = 0
        l = len(data)
        # for each row/column, we check if it's a mirror
        for i in range(l):
            if i + 1 == ignore:
                continue

            next = range(i + 1, l)
            prev = range(i, -1, -1)
            isref = False
            # Iterate forward and backward at the same time and check the char
            # to see if it's a reflection:
            # i = 4 -> next = [4,3,2,1,0], prev = [5,6,7,8,9]
            # Two pointers, one forward and the other backward
            for j, k in zip(prev, next):
                if data[j] != data[k]:
                    isref = False
                    break
                isref = True
            if isref:
                n = i + 1
                break

        return n

    def fix_smudge(self, ignore):
        n = 0
        data = self.rows
        data1 = [list(i) for i in self.rows]
        data2 = [list(i) for i in self.columns]
        ig, dir = ignore

        ni = len(data)
        nj = len(data[0])
        # iterate through all points and try inverting
        for i in range(ni):
            for j in range(nj):
                v = data1[i][j]
                if v == "#":
                    data1[i][j] = "."
                    data2[j][i] = "."
                else:
                    data1[i][j] = "#"
                    data2[j][i] = "#"
                x = self._ref(data2, ignore=ig if dir == V else None)
                if x:
                    return x, (i, j)
                y = self._ref(data1, ignore=ig if dir == H else None)
                if y:
                    return y * 100, (i, j)

                data1[i][j] = v
                data2[j][i] = v

        return n

    def __repr__(self):
        return "\n".join(self.rows)


class D13(Problem):
    def solve_p1(self):
        n = 0
        for p in self.patterns:
            n1, n2 = 0, 0
            n1 = p.reflection(H) * 100
            if not n1:
                n2 = p.reflection(V)
            n += n1 + n2

        return n

    def solve_p2(self):
        n = 0
        for p in self.patterns:
            n3, n4 = 0, 0
            n1 = p.reflection(H)
            if n1:
                n3 = p.fix_smudge((n1, H))[0]
            else:
                n2 = p.reflection(V)
                n4 = p.fix_smudge((n2, V))[0]
            n += n3 + n4
        return n

    def parseinput(self, lines):
        data = [i.strip() for i in lines]
        self.patterns = []
        p = []
        for d in data[1:]:
            if not d:
                self.patterns.append(Pattern(p))
                p = []
                continue
            p.append(d)
        # the last one
        self.patterns.append(Pattern(p))

        return data


if __name__ == "__main__":
    print("Day 13: Point of Incident")

    p = D13("d13.data")
    print(p.solve_p1())
    print(p.solve_p2())
