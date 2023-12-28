import networkx as nx
from base import Problem


example = """
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


def test_part1():
    p = D25(example)
    assert set(p.graph["jqt"]) == {"rhn", "xhk", "nvd", "ntq"}
    assert set(p.graph["ntq"]) == {"jqt", "hfx", "bvb", "xhk"}
    assert nx.edge_connectivity(p.graph) == 3
    assert p.solve_p1() == 54


def test_part2():
    p = D25(example)
    assert p.solve_p2() == 0


class D25(Problem):
    def solve_p1(self):
        G = self.graph.copy()
        cut = nx.minimum_edge_cut(G)
        G.remove_edges_from(cut)
        n = 1
        for i in nx.connected_components(G):
            n *= len(i)
        return n

    def solve_p2(self):
        return 0

    def parseinput(self, lines):
        data = tuple(i.strip() for i in lines if i.strip())
        graph = nx.Graph()

        for line in data:
            node, connections = line.split(":")
            connections = set(i.strip() for i in connections.split())
            graph.add_node(node)
            for n in connections:
                graph.add_edge(node, n)

        self.graph = graph
        return data


if __name__ == "__main__":
    print("Day 25: Snowverload")

    p = D25("d25.data")
    print(p.solve_p1())
    print(p.solve_p2())
