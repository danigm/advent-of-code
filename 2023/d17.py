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

HEAT_LOSS_LIMIT = 3


class Top:
    @classmethod
    def next(cls, r, c):
        return r - 1, c
    @classmethod
    def left(cls):
        return Left
    @classmethod
    def right(cls):
        return Right

class Bottom:
    @classmethod
    def next(cls, r, c):
        return r + 1, c
    @classmethod
    def left(cls):
        return Right
    @classmethod
    def right(cls):
        return Left

class Left:
    @classmethod
    def next(cls, r, c):
        return r, c - 1
    @classmethod
    def left(cls):
        return Bottom
    @classmethod
    def right(cls):
        return Top

class Right:
    @classmethod
    def next(cls, r, c):
        return r, c + 1
    @classmethod
    def left(cls):
        return Top
    @classmethod
    def right(cls):
        return Bottom


def test_part1():
    p = D17(example)
    assert p.solve_p1() == 102


def test_part2():
    p = D17(example)
    assert p.solve_p2() == 0


class Node:
    def __init__(self, r, c, steps, dir):
        self.r = r
        self.c = c
        self.steps = steps
        self.dir = dir

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self.r, self.c) == tuple
        return (self.r, self.c) == (other.r, other.c)

    def __lt__(self, other):
        return (self.r, self.c) < (other.r, other.c)

    def __gt__(self, other):
        return (self.r, self.c) > (other.r, other.c)

    def __hash__(self):
        return hash((self.r, self.c))

    def __repr__(self):
        return repr((self.r, self.c, self.steps))


class D17(Problem):
    def solve_p1(self):
        return self.minimize_heat_loss(0, 0, dir=Right)

    def rank(self, queue, r, c):
        r = []
        for i in queue:
            r, c = i.next(r, c)
            pos = self.data[r][c]
            r.append(pos)

    def heat_loss(self, came_from, current):
        n = self.data[current[0]][current[1]]
        while current in came_from:
            v = self.data[current[0]][current[1]]
            print(current, v, n)
            current = came_from[current]
            n += self.data[current[0]][current[1]]
        return n

    def h(self, r, c, came_from):
        n = self.heat_loss(came_from, (r, c))
        dr, dc = self.destination
        return (abs(dr - r) + abs(dc - c)) + n

    # A*, https://en.wikipedia.org/wiki/A*_search_algorithm
    def minimize_heat_loss(self, r, c, dir=Right):
        open_set = [Node(r,c, 0, dir)]
        came_from = {}
        # cost of the cheapest path, defaults to infinity
        g_score = {}
        g_score[(r,c)] = 0

        # f_score[n] = g_score[n] + h(n)
        f_score = {}
        # Do not count the start block
        f_score[(r,c)] = 0
        block = self.data[r][c]

        while open_set:
            # get the value with lowest f_score, open_set is sorted by f_score
            node = open_set.pop(0)
            nd = node.dir
            steps = node.steps
            current = (node.r, node.c)
            if current == self.destination:
                if open_set:
                    print("NOT COMPLETE", open_set)
                    print(f_score)
                return self.heat_loss(came_from, current)

            neighbors = [(nd, steps + 1), (nd.left(), 1), (nd.right(), 1)]

            for d, st in neighbors:
                if st > 3:
                    # ignore this possibility
                    continue
                nr, nc = d.next(*current)
                if nr < 0 or nc < 0 or nr >= self.rows or nc >= self.cols:
                    # Out of bounds
                    continue
                block = self.data[nr][nc]
                print(d, block, (nr,nc), st)
                print(open_set)

                tentative_g_score = g_score.get(current, math.inf) + block
                if tentative_g_score < g_score.get((nr, nc), math.inf):
                    came_from[(nr, nc)] = current
                    g_score[(nr, nc)] = tentative_g_score
                    f_score[(nr, nc)] = tentative_g_score + self.h(nr, nc, came_from)
                    if (nr, nc) not in open_set:
                        open_set = sorted([Node(nr, nc, st, d)] + open_set, key=lambda x: f_score.get(x, math.inf))

        return math.inf

    # Recursive approach
    #@lru_cache
    #def minimize_heat_loss(self, r, c, direction=Right, steps=0):
    #    print(r, c, direction, steps)
    #    if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
    #        return math.inf
    #    block = self.data[r][c]
    #    if (r, c) == self.destination:
    #        return block

    #    n1, n2, n3 = math.inf, math.inf, math.inf

    #    # Continue
    #    if steps < HEAT_LOSS_LIMIT:
    #        # can continue same direction
    #        nr, nc = direction.next(r, c)
    #        n1 = self.minimize_heat_loss(nr, nc, direction, steps + 1)
    #    # Turn left
    #    nd = direction.left()
    #    nr, nc = nd.next(r, c)
    #    n2 = self.minimize_heat_loss(nr, nc, nd, 1)
    #    # Turn right
    #    nd = direction.right()
    #    nr, nc = nd.next(r, c)
    #    n3 = self.minimize_heat_loss(nr, nc, nd, 1)

    #    return block + min(n1, n2, n3)

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        data = tuple(tuple(int(j) for j in tuple(i.strip())) for i in lines if i.strip())
        self.rows = len(data)
        self.cols = len(data[0])
        self.destination = (self.rows - 1, self.cols - 1)
        return data


if __name__ == "__main__":
    print("Day 17: ")

    p = D17("d17.data")
    print(p.solve_p1())
    print(p.solve_p2())
