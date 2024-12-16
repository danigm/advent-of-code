import heapq
from collections import defaultdict
from functools import lru_cache
from base import Problem


example = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

example2 = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


D = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1),
}

DR = {
    "N": "WE",
    "S": "WE",
    "E": "NS",
    "W": "NS",
}


def test_part1():
    p = D16(example)
    assert p.solve_p1() == 7036
    p = D16(example2)
    assert p.solve_p1() == 11048


def test_part2():
    p = D16(example)
    assert p.solve_p2() == 45
    p = D16(example2)
    assert p.solve_p2() == 64


@lru_cache(maxsize=None)
def possibles(pos, map):
    s, i, j, d = pos
    di, dj = D[d]
    ni, nj = i + di, j + dj

    p = []
    if map[ni][nj] != "#":
        p.append((s+1, ni, nj, d))
    for nd in DR[d]:
        p.append((s+1000, i, j, nd))

    return p


class D16(Problem):
    def search(self, s, map):
        queue = [s]
        score = 0
        visited = set()
        ends = []
        end_score = None
        scores = defaultdict(list)
        while queue:
            score, i, j, d = heapq.heappop(queue)
            visited.add((i, j, d))

            if end_score is not None and score > end_score:
                continue

            if (i, j) == self.end:
                ends.append((score, i, j, d))
                end_score = score
                continue

            prev = (score, i, j, d)
            for p in possibles(prev, map):
                s, i, j, d = p
                scores[(s, i, j, d)].append(prev)
                if (i, j, d) not in visited:
                    heapq.heappush(queue, p)

        path = set()
        queue = ends
        visited = set()
        while queue:
            n = queue.pop()
            s, i, j, d = n
            path.add((i, j))
            if (i, j) == self.start and s == 0:
                continue
            if n in visited:
                continue
            visited.add(n)
            queue += scores[n]
        return end_score, path

    def solve_p1(self):
        map = self.data
        s = 0, *self.start, "E"
        score, _ = self.search(s, map)
        return score

    def solve_p2(self):
        map = self.data
        s = 0, *self.start, "E"
        _, p = self.search(s, map)
        return len(p)

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        self.start = 0, 0
        self.end = 0, 0
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                if c == "S":
                    self.start = i, j
                if c == "E":
                    self.end = i, j
        return data


if __name__ == "__main__":
    print("Day 16: Reindeer Maze")

    p = D16("d16.data")
    print(p.solve_p1())
    print(p.solve_p2())
