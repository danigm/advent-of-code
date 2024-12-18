import math
import heapq
from base import Problem


example = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_part1():
    p = D18(example, size=7)
    assert p.solve_p1(12) == 22


def test_part2():
    p = D18(example, size=7)
    assert p.solve_p2() == "6,1"


class D18(Problem):
    def __init__(self, *args, size=71):
        super().__init__(*args)
        self.size = size

    def possibles(self, pos, corrupt):
        x, y = pos
        s = self.size
        p = [
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1),
        ]
        p = filter(lambda x: x not in corrupt, p)
        p = filter(lambda x: 0 <= x[0] < s and 0 <= x[1] < s, p)
        return p

    def draw(self, corrupt, visited, u=None):
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == u:
                    print("@", end="")
                elif (x, y) in corrupt:
                    print("#", end="")
                elif (x, y) in visited:
                    print("O", end="")
                else:
                    print(".", end="")
            print("\n", end="")

    def find(self, start, end, corrupt):
        visited = set()

        d = math.dist(start, end)
        queue = [(d, 0, start)]
        possible = False
        while queue:
            d, steps, u = heapq.heappop(queue)
            if u in visited:
                continue
            visited.add(u)

            # self.draw(corrupt, visited, u)
            if u == end:
                possible = True
                break

            for p in self.possibles(u, corrupt | visited):
                d = math.dist(p, end) + steps + 1
                heapq.heappush(queue, (d, steps + 1, p))
            
        return steps, possible

    def solve_p1(self, b=1024):
        s, e = (0, 0), (self.size - 1, self.size - 1)
        corrupt = set(self.data[0:b])

        steps, _ = self.find(s, e, corrupt)
        return steps

    def solve_p2(self):
        s, e = (0, 0), (self.size - 1, self.size - 1)
        l = len(self.data)
        for c in range(l):
            corrupt = set(self.data[0:l - c])
            _, possible = self.find(s, e, corrupt)
            if possible:
                return ",".join(map(str, self.data[l - c]))

        return None

    def parseinput(self, lines):
        data = tuple(tuple(map(int, i.strip().split(","))) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 18: RAM Run")

    p = D18("d18.data")
    print(p.solve_p1())
    print(p.solve_p2())
