from base import Problem


example = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""


def test_part1():
    p = D06(example)
    assert p.solve_p1() == 41


def test_part2():
    p = D06(example)
    assert p.solve_p2() == 6


class D06(Problem):
    def _move(self, direction, pos, visited):
        """
        * If there is something directly in front of you, turn right 90
          degrees.
        * Otherwise, take a step forward.
        """
        i, j = pos
        di, dj = 0, 0
        end = 0
        if direction == 0:
            di = -1
            end = -1
        elif direction == 1:
            dj = 1
            end = self.width
        elif direction == 2:
            di = 1
            end = self.height
        elif direction == 3:
            dj = -1
            end = -1

        steps = 0
        # Find next obstacle
        while i != end and j != end:
            visited.add((i, j))
            if (i, j, direction) in self.passt:
                raise Exception("LOOP!")
            self.passt.add((i, j, direction))
            if (i+di, j+dj) in self.obstacles:
                break
            i += di
            j += dj
            steps += 1

        if i == end or j == end:
            return None, (i - di, j - dj), steps - 1

        return (i+di, j+dj), (i, j), steps

    def solve_p1(self):
        self.passt = set()
        direction = 0
        total = 0
        visited = set()
        pos = self.pos
        obstacle, pos, steps = self._move(direction, pos, visited)
        total += steps
        while obstacle is not None:
            # Turn right
            direction = (direction + 1) % 4
            obstacle, pos, steps = self._move(direction, pos, visited)
            total += steps
        self.visited = visited
        return len(visited)

    def solve_p2(self):
        # To get all visited positions
        self.solve_p1()
        visited = self.visited

        loops = 0
        for (i, j) in visited:
            self.obstacles.add((i, j))
            try:
                self.solve_p1()
            except Exception as e:
                loops += 1
            self.obstacles.remove((i, j))
                
        return loops

    def parseinput(self, lines):
        self.pos = (0, 0)
        self.obstacles = set()
        self.original = []
        self.width = 0
        self.height = 0
        i = 0
        for line in lines:
            l = line.strip()
            if not l:
                continue
            line = []
            for j, c in enumerate(l):
                if "^" == c:
                    self.pos = (i, j)
                if "#" == c:
                    self.obstacles.add((i, j))
                line.append(c)
            self.original.append(line)
            i += 1

        self.width = len(self.original[0])
        self.height = len(self.original)
        return self.original


if __name__ == "__main__":
    print("Day 06: Guard Gallivant")

    p = D06("d06.data")
    print(p.solve_p1())
    p = D06("d06.data")
    print(p.solve_p2())
