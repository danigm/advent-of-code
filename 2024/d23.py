import networkx as nx
from base import Problem


example = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def all_connected(g, n):
    for i, c1 in enumerate(n):
        for c2 in n[i+1:]:
            if not g.has_edge(c1, c2):
                return False
    return True


def connected(g, nodes=None):
    nets = set()
    bignets = set()
    if nodes is None:
        nodes = g

    # for each node, get all connected
    # for each connected get following nodes and keep just the nodes that are
    # also connected to the first one
    for c in nodes:
        net = set(g[c])
        comb = net
        for c1 in net:
            cnet = set(g[c1])
            comb = net & cnet
            bignets.add(tuple(sorted((c, c1, *comb))))
            for c2 in comb:
                nets.add(tuple(sorted((c, c1, c2))))

    # Filter nets that are not fully connected
    for n in list(bignets):
        # All nodes connected with all nodes
        if not all_connected(g, n):
            bignets.remove(n)

    return nets, bignets


def test_part1():
    p = D23(example)
    n, _ = connected(p.g)
    assert len(n) == 12
    assert p.solve_p1() == 7


def test_part2():
    p = D23(example)
    assert p.solve_p2() == "co,de,ka,ta"


class D23(Problem):
    def solve_p1(self):
        nodes = (i for i in self.g if i.startswith("t"))
        n, _ = connected(self.g, nodes)
        return len(n)

    def solve_p2(self):
        _, p = connected(self.g)
        p = sorted(p, key=len)[-1]
        return ",".join(p)

    def parseinput(self, lines):
        self.g = nx.Graph()
        for line in lines:
            l = line.strip()
            if not l:
                continue
            c1, c2 = l.split("-")
            self.g.add_node(c1)
            self.g.add_node(c2)
            self.g.add_edge(c1, c2)

        return self.g


if __name__ == "__main__":
    print("Day 23: LAN Party")

    p = D23("d23.data")
    print(p.solve_p1())
    print(p.solve_p2())
