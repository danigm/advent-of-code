from base import Problem


example = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_part1():
    p = D10(example)
    assert p.solve_p1() == 36


def test_part2():
    p = D10(example)
    assert p.solve_p2() == 81


class D10(Problem):
    def rating(self, pos):
        pass

    def score(self, pos, prev=None, visited=None, rating=False):
        i, j = pos
        if i >= self.height or i < 0:
            return 0
        if j >= self.width or j < 0:
            return 0

        # Do not count same path
        if visited and (i, j) in visited:
            return 0
        if visited is None:
            visited = set()

        v = self.data[i][j]
        if prev is not None and v - prev != 1:
            return 0

        if v == 9:
            if not rating:
                visited.add((i, j))
            return 1

        total = 0
        p1 = i - 1, j
        p2 = i + 1, j
        p3 = i, j - 1
        p4 = i, j + 1
        total += self.score(p1, v, visited, rating)
        total += self.score(p2, v, visited, rating)
        total += self.score(p3, v, visited, rating)
        total += self.score(p4, v, visited, rating)

        return total

    def solve_p1(self):
        total = 0
        for i, line in enumerate(self.data):
            for j, n in enumerate(line):
                if n != 0:
                    continue
                total += self.score((i, j))
        return total

    def solve_p2(self):
        total = 0
        for i, line in enumerate(self.data):
            for j, n in enumerate(line):
                if n != 0:
                    continue
                total += self.score((i, j), rating=True)
        return total

    def parseinput(self, lines):
        data = tuple(tuple(int(j) for j in i.strip()) for i in lines if i.strip())
        self.height = len(data)
        self.width = len(data[0])
        return data


if __name__ == "__main__":
    print("Day 10: Hoof It")

    p = D10("d10.data")
    print(p.solve_p1())
    print(p.solve_p2())
