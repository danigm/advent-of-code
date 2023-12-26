from collections import defaultdict
from base import Problem


example = """
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


def test_part1():
    p = D23(example)
    p.build_graph()
    assert p.start == (0, 1)
    assert p.end == (p.rows - 1, p.cols - 2)
    assert p.end == (p.rows - 1, p.cols - 2)
    assert p.graph[p.start] == {((5, 3), 15)}
    assert p.graph[(5, 3)] == {((3, 11), 22), ((13, 5), 22)}
    assert p.graph[p.end] == set()
    assert p.ingraph[p.end] == {((3, 11), 45), ((13, 5), 53), ((13, 13), 33), ((13, 13), 25)}
    assert p.longest_path() == 94
    assert p.solve_p1() == 94


def test_part2():
    p = D23(example)
    assert p.solve_p2() == 0


def get_neighbors(node, data, visited):
    r, c = node
    rows = len(data)
    cols = len(data[0])
    t = data[r][c]

    neighbors = ((0, 1), (0, -1), (1, 0), (-1, 0))
    possible = {
        ".": ((0, 1), (0, -1), (1, 0), (-1, 0)),
        ">": ((0, 1),          (1, 0), (-1, 0)),
        "<": (        (0, -1), (1, 0), (-1, 0)),
        "^": ((0, 1), (0, -1),         (-1, 0)),
        "v": ((0, 1), (0, -1), (1, 0)         ),
    }

    ns = []
    for (xr, xc) in neighbors:
        nr, nc = xr + r, xc + c
        if not (0 <= nr < rows and 0 <= nc < cols):
            continue
        if data[nr][nc] == "#":
            continue
        if (nr, nc) in visited:
            continue
        x = data[nr][nc]
        if (xr, xc) not in possible[x]:
            continue
        ns.append((nr, nc))

    return set(ns)


class D23(Problem):
    def solve_p1(self):
        self.build_graph()
        return self.longest_path()

    def solve_p2(self):
        return 0

    # https://en.wikipedia.org/wiki/Longest_path_problem
    def longest_path(self):
        l = self.topological_order()
        lengths = {}
        for v in l:
            inv = self.ingraph[v]
            if not inv:
                n = 0
            else:
                n = max(i[1] + lengths.get(i[0], 0) for i in inv)

            lengths[v] = n

        return lengths[self.end]

    # https://en.wikipedia.org/wiki/Topological_sorting
    def topological_order(self):
        # L ← Empty list that will contain the sorted elements
        l = []
        # S ← Set of all nodes with no incoming edge
        s = {self.start}
        visited = {self.start}

        # while S is not empty do
        while s:
            # remove a node n from S
            n = s.pop()
            visited.add(n)
            # add n to L
            l.append(n)
            # for each node m with an edge e from n to m do
            neighbors = self.graph[n]
            for (m, nm) in neighbors:
                # remove edge e from the graph
                other_nodes = [i for i in self.ingraph[m] if i[0] not in visited]
                # if m has no other incoming edges then
                if not other_nodes:
                    # insert m into S
                    s.add(m)

        return l

    def find_next_node(self, node, visited=None):
        data = self.data
        visited = visited or {node}
        next_node = node
        ns = get_neighbors(node, data, visited)
        visited.add(node)
        n = 0
        while len(ns) == 1:
            n += 1
            next_node = ns.pop()
            visited.add(next_node)
            ns = get_neighbors(next_node, data, visited)

        return (next_node, n)

    def build_graph(self):
        data = self.data
        rows = len(data)
        cols = len(data[0])
        graph = defaultdict(set)
        ingraph = defaultdict(set)
        start = (0, data[0].index("."))
        end = (rows - 1, data[-1].index("."))
        ns = get_neighbors(start, data, {start})
        to_consider = [(i, start) for i in ns]

        while to_consider:
            node, current = to_consider.pop(0)
            next_node, n = self.find_next_node(node, {current})
            # intersection, new node!
            graph[current].add((next_node, n + 1))
            ingraph[next_node].add((current, n + 1))

            if next_node != end:
                ns = get_neighbors(next_node, data, {node})
                to_consider += [(i, next_node) for i in ns if i not in graph]

        self.graph = graph
        self.ingraph = ingraph
        self.rows = rows
        self.cols = cols
        self.start = start
        self.end = end

    def parseinput(self, lines):
        data = tuple(tuple(i.strip()) for i in lines if i.strip())
        return data


if __name__ == "__main__":
    print("Day 23: A Long Walk")

    p = D23("d23.data")
    print(p.solve_p1())
    print(p.solve_p2())
