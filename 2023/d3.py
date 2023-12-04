from base import Problem


example = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def test_d3():
    p = D3(example)
    assert p.solve_p1() == 4361

    p = D3(example)
    assert p.solve_p2() == 467835
    assert len(p.gears) == 3
    gears = [i for i in p.gears.values() if i.is_gear()]
    assert len(gears) == 2
    assert gears[0].ratio() == 16345
    assert gears[1].ratio() == 451490


def is_number(char):
    return "0" <= char <= "9"


class Gear:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.adjacents = []

    def is_gear(self):
        return len(self.adjacents) == 2

    def ratio(self):
        if not self.is_gear():
            return 0
        x, y = self.adjacents
        return x * y

    def __repr__(self):
        return f"({self.i}, {self.j}) {self.adjacents}"

    def __str__(self):
        return f"({self.i}, {self.j}) {self.adjacents}"


class D3(Problem):
    def __init__(self, input):
        super().__init__(input)
        self.gears = {}

    def solve_p1(self):
        return sum(self.adjacent_numbers())

    def solve_p2(self):
        adjacents = self.adjacent_numbers()
        return sum(g.ratio() for g in self.gears.values() if g.is_gear())

    def is_part_number(self, i, j1, j2):
        """
        Look for adjacent symbols, not a number of "."
        """

        part_number = False
        row = self.data[i]
        number = int(''.join(row[j1:j2]))
        left = j1
        right = j2

        if j1:
            left = j1 - 1
        if j2 < len(row) - 1:
            right = j2 + 1

        i1 = i
        i2 = i

        # upper row
        if i:
            i1 = i - 1
        # lower row
        if i < len(self.data) - 1:
            i2 = i + 1

        for x in range(i1, i2 + 1):
            for y in range(left, right):
                symbol = self.data[x][y]
                if not (symbol == "." or is_number(symbol)):
                    part_number = True
                if self.data[x][y] == "*":
                    gear = self.gears.get((x, y), Gear(x, y))
                    gear.adjacents.append(number)
                    self.gears[(x, y)] = gear

        return part_number

    def adjacent_numbers(self):
        numbers = []

        for i, row in enumerate(self.data):
            j1, j2 = None, None
            for j, symbol in enumerate(row):
                if symbol == "*":
                    if not (i, j) in self.gears:
                        self.gears[(i, j)] = Gear(i, j)
                if is_number(symbol):
                    if j1 is None:
                        j1 = j
                    j2 = j
                    continue

                # Not a number
                if j1 is None:
                    continue
                if j2:
                    j2 += 1

                # A complete number
                if self.is_part_number(i, j1, j2):
                    numbers.append(int(''.join(row[j1:j2])))
                j1, j2 = None, None

            if j1 is not None:
                if j2:
                    j2 += 1
                # The last number
                if self.is_part_number(i, j1, j2):
                    numbers.append(int(''.join(row[j1:j2])))

        return numbers


if __name__ == "__main__":
    print("Day 3: Gear Ratios")

    p = D3("d3.data")
    print(p.solve_p1())
    p = D3("d3.data")
    print(p.solve_p2())
