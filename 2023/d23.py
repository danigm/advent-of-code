import heapq
import math
import copy
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
    p.build_graph(slopes=False)
    for n in p.graph:
        inv = {i[0] for i in p.ingraph[n]}
        inv1 = {i for i in p.graph if n in {j[0] for j in p.graph[i]}}
        assert inv == inv1
    assert p.solve_p2() == 154


class D23(Problem):
    def solve_p1(self):
        self.build_graph()
        return self.longest_path()

    def solve_p2(self):
        self.build_graph(slopes=False)
        return self.dijkstra(self.start)

    def edge(self, n1, n2):
        for (n, d) in self.graph[n1]:
            if n == n2:
                return d

    def distance(self, path):
        n = 0
        for i in range(0, len(path) - 1):
            n1 = path[i]
            n2 = path[i + 1]
            n += self.edge(n1, n2)
        return n

    def dijkstra(self, source):
        # NOT working because I'm not evaluating the restriction of not
        # repeating nodes to calculate the longest path
        graph = self.graph
        dist = {}
        prev = {}
        queue = []
        q = {self.start, self.end}
        # for each vertex v in Graph.Vertices:
        for v in graph:
            dist[v] = math.inf
            prev[v] = None
            q.add(v)
        dist[source] = 0
        dist[self.end] = math.inf
        heapq.heappush(queue, (0, source, []))
        q.add(source)

        # while Q is not empty:
        while queue:
            # u ← vertex in Q with min dist[u]
            u = heapq.heappop(queue)
            distance, u, path = u
            # remove u from Q
            # q.remove(u)
            # for each neighbor v of u still in Q:
            neighbors = [i for i in graph[u] if i[0] not in path]

            if u == self.end:
                alt = -self.distance(path + [u])
                if alt < dist[u]:
                    dist[u] = alt

            for (v, n) in neighbors:
                alt = -self.distance(path + [u, v])
                # alt ← dist[u] + Graph.Edges(u, v)
                # alt = distance - n
                # if alt < dist[v]:
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                heapq.heappush(queue, (alt, v, path + [u]))

        return -dist[self.end]

# 1  S ← empty sequence
# 2  u ← target
# 3  if prev[u] is defined or u = source:          // Do something only if the vertex is reachable
# 4      while u is defined:                       // Construct the shortest path with a stack S
# 5          insert u at the beginning of S        // Push the vertex onto the stack
# 6          u ← prev[u]                           // Traverse from target to source


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

        g = copy.deepcopy(self.graph)
        ig = copy.deepcopy(self.ingraph)

        # while S is not empty do
        while s:
            # remove a node n from S
            n = s.pop()
            visited.add(n)
            # add n to L
            l.append(n)
            # for each node m with an edge e from n to m do
            neighbors = list(g[n])
            for (m, nm) in neighbors:
                # remove edge e from the graph
                g[n].remove((m, nm))
                ig[m].remove((n, nm))
                other_nodes = [i for i in ig[m] if i[0] not in visited]
                # if m has no other incoming edges then
                if not other_nodes:
                    # insert m into S
                    s.add(m)

        return l

    def get_neighbors(self, node, visited):
        r, c = node
        data = self.data
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
            if self.slopes and (xr, xc) not in possible[x]:
                continue
            ns.append((nr, nc))

        return set(ns)

    def find_next_node(self, node, visited=None):
        data = self.data
        visited = visited or {node}
        next_node = node
        ns = self.get_neighbors(node, visited)
        visited.add(node)
        n = 0
        while len(ns) == 1:
            n += 1
            next_node = ns.pop()
            visited.add(next_node)
            ns = self.get_neighbors(next_node, visited)

        return (next_node, n)

    def build_graph(self, slopes=True):
        self.slopes = slopes
        data = self.data
        rows = len(data)
        cols = len(data[0])
        graph = defaultdict(set)
        ingraph = defaultdict(set)
        start = (0, data[0].index("."))
        end = (rows - 1, data[-1].index("."))
        ns = self.get_neighbors(start, {start})
        to_consider = [(i, start) for i in ns]
        visited = set()

        while to_consider:
            node, current = to_consider.pop(0)
            visited.add(node)
            next_node, n = self.find_next_node(node, {current})
            # intersection, new node!
            graph[current].add((next_node, n + 1))
            ingraph[next_node].add((current, n + 1))

            if next_node != end:
                ns = self.get_neighbors(next_node, {node})
                to_consider += [(i, next_node) for i in ns if i not in graph and i not in visited]

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
