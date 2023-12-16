from base import Problem


example = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


North = 0
South = 1
West = 2
East = 3


def test_part1():
    p = D14(example)
    assert p.solve_p1() == 136


def test_part2():
    p = D14(example)
    assert p.solve_p2() == 0


class D14(Problem):
    def solve_p1(self):
        return self.tilt(North)

    def solve_p2(self):
        return 0

    def tilt(self, direction=North):
        R = len(self.data)
        C = len(self.data[0])

        L = C
        if direction in [North, South]:
            L = R

        n = 0
        for i in range(R):
            load = L
            for j in range(C):
                if direction == North:
                    rock = self.data[j][i]
                elif direction == South:
                    rock = self.data[-(j + 1)][i]
                elif direction == West:
                    rock = self.data[i][j]
                else:
                    rock = self.data[-(i+1)][j]

                if rock == "#":
                    # solid rock
                    load = L - (j + 1)
                    continue
                if rock == "O":
                    n += load
                    # rounded rock
                    load -= 1
                    continue

        return n

    def parseinput(self, lines):
        data = [list(i.strip()) for i in lines if i.strip()]
        return data


if __name__ == "__main__":
    print("Day 14: Parabolic Reflector Dish")

    p = D14("d14.data")
    print(p.solve_p1())
    print(p.solve_p2())
