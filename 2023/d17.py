import heapq
import math
from functools import lru_cache
from base import Problem


example = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

example_xs = """
24134323113
32154535356
32552456542
34465858454
"""

HEAT_LOSS_LIMIT = 3


Top = 1
Bottom = 2
Left = 3
Right = 4


def test_part1():
    # p = D17(example_xs)
    # assert p.solve_p1() == 47
    p = D17(example)
    assert p.solve_p1() == 102


def test_part2():
    p = D17(example)
    assert p.solve_p2() == 0


class D17(Problem):
    def solve_p1(self):
        return self.minimize_heat_loss()

    # Dijkstra alg
    # https://en.wikipedia.org/wiki/Dijkstra's_algorithm
    def minimize_heat_loss(self):
        dist = {}
        queue = []
        for i in range(self.rows):
            for j in range(self.cols):
                for d in [Top, Bottom, Left, Right]:
                    for s in range(1, 4):
                        v = (i, j, d, s)
                        dist[v] = math.inf

        for i in range(4):
            dist[(0,0,0,i)] = 0
        queue.append((0,0,0,0,1))

        while queue:
            # vertex with min dist[u]
            u = heapq.heappop(queue)

            distance, r, c, d, s = u
            sb = s + 1 if d == Bottom else 1
            st = s + 1 if d == Top else 1
            sr = s + 1 if d == Right else 1
            sl = s + 1 if d == Left else 1

            if (r, c) == self.destination:
                return distance

            neighbors = [(r+1,c,Bottom,sb), (r,c+1,Right,sr)]
            if d == Top:
                neighbors = [(r-1,c,Top,st), (r,c+1,Right,sr), (r,c-1,Left,sl)]
            if d == Bottom:
                neighbors = [(r+1,c,Bottom,sb), (r,c+1,Right,sr), (r,c-1,Left,sl)]
            if d == Left:
                neighbors = [(r+1,c,Bottom,sb), (r-1,c,Top,st), (r,c-1,Left,sl)]
            if d == Right:
                neighbors = [(r+1,c,Bottom,sb), (r-1,c,Top,st), (r,c+1,Right,sr)]

            for v in neighbors:
                nr, nc, d,s = v
                if s >= 4:
                    continue

                if nr < 0 or nc < 0 or nr >= self.rows or nc >= self.cols:
                    continue

                alt = distance + self.data[nr][nc]
                if alt < dist[v]:
                    dist[v] = alt
                    # sort by min dist[u]
                    heapq.heappush(queue, (alt, nr, nc, d, s))

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        data = tuple(tuple(int(j) for j in tuple(i.strip())) for i in lines if i.strip())
        self.rows = len(data)
        self.cols = len(data[0])
        self.destination = (self.rows - 1, self.cols - 1)
        return data


if __name__ == "__main__":
    print("Day 17: Clumsy Crucible")

    p = D17("d17.data")
    print(p.solve_p1())
    print(p.solve_p2())
