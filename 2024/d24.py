import re
import operator
import itertools
from collections import defaultdict
from base import Problem


G = re.compile(r"(\w+\d*) (AND|OR|XOR) (\w+\d*) -> (\w+\d*)")


example = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""


example2 = """
x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""


example3 = """
x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00
"""


OP = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
}


def test_part1():
    p = D24(example2)
    assert p.solve_p1() == 4
    p = D24(example)
    assert p.solve_p1() == 2024


def test_part2():
    p = D24(example3)
    a = int("101010", 2)
    b = int("101100", 2)
    assert p.solve_p2(operator.and_, 2) == "z00,z01,z02,z05"


def number(wires, key="x"):
    out = []
    for u in wires:
        if u.startswith(key):
            out.append((u, wires[u]))

    n = int("".join((str(i) for k, i in reversed(sorted(out)))), 2)
    return n


def set_number(wires, n, key="x"):
    bytes = f"{n:b}"
    for i, b in enumerate(reversed(bytes)):
        k = f"{key}{i:02}"
        wires[k] = int(b)


def valid(comb):
    visited = set()
    for c1, c2 in comb:
        if c1 in visited or c2 in visited:
            return False
        visited.add(c1)
        visited.add(c2)
    return True


def path(x, wrongs):
    if x not in wrongs:
        return []

    a, b = wrongs[x]
    return [x] + path(a, wrongs) + path(b, wrongs)


def p2_brute_force(self, op, nswaps):
    wires = {k: v for k, v in iwires.items()}
    gates = {k: v for k, v in igates.items()}
    x = self.solve_p1(wires, gates)
    swaps = list(itertools.combinations(sorted(gates.keys()), 2))
    print("SWAPS")
    for s in itertools.permutations(gates, nswaps*2):
        for o1, o2 in itertools.pairwise(s):
            print("PERM:", o1, o2)
            gates[o1], gates[o2] = gates[o2], gates[o1]

        x = self.solve_p1(wires, gates)
        if x == out:
            break
        wires = {k: v for k, v in iwires.items()}
        gates = {k: v for k, v in igates.items()}

    return ",".join(sorted(s))


class D24(Problem):
    def solve_p1(self, wires=None, gates=None):
        iwires, igates, initial = self.data
        if wires is None:
            wires = iwires
        if gates is None:
            gates = igates
        unknown = set(gates.keys())

        while unknown:
            for u in tuple(unknown):
                op, a, b = gates[u]
                if a in wires and b in wires:
                    a = wires[a]
                    b = wires[b]
                    wires[u] = OP[op](a, b)
                    unknown.remove(u)

        return number(wires, "z")

    def solve_p2(self, op, nswaps=4):
        # https://www.electronics-lab.com/article/binary-adder/
        wires, gates, initial = self.data
        n1 = number(wires, "x")
        n2 = number(wires, "y")
        out = op(n1, n2)
        set_number(wires, out, "z")

        wrongs = set()
        for g in gates:
            op, a, b = gates[g]
            if a in gates and b in gates:
                # xor & or
                op1, *_ = gates[a]
                op2, *_ = gates[b]
            # last one, carry
            if g == "z45" and op != "OR":
                wrongs.add(g)
                continue

            if g != "z45" and g.startswith("z") and op != "XOR":
                wrongs.add(g)
                continue

            if op == "OR":
                # and & and
                op1, *_ = gates[a]
                op2, *_ = gates[b]
                if op1 != "AND":
                    wrongs.add(a)
                if op2 != "AND":
                    wrongs.add(b)

            if op == "XOR":
                if a in gates and b in gates:
                    # xor & or
                    op1, *_ = gates[a]
                    op2, *_ = gates[b]

                    pattern = ("OR", "XOR")
                    if g == "z01":
                        pattern = ("AND", "XOR")

                    if tuple(sorted((op1, op2))) != pattern:
                        if op1 in pattern and op2 in pattern:
                            wrongs.add(f"{a}|{b}")
                        elif op1 in pattern:
                            wrongs.add(b)
                        elif op2 in pattern:
                            wrongs.add(a)
                        else:
                            wrongs.add(a)
                            wrongs.add(b)

        return ",".join(sorted(wrongs))


    def parseinput(self, lines):
        wires = {}
        gates = {}
        for line in lines:
            l = line.strip()
            if not l:
                continue

            if ":" in l:
                w, n = l.split(": ")
                n = int(n)
                wires[w] = n
            else:
                m = G.match(l)
                a, op, b, out = m.groups()
                gates[out] = (op, a, b)

        initial = tuple(wires.keys())
        return wires, gates, initial


if __name__ == "__main__":
    print("Day 24: Crossed Wires")

    p = D24("d24.data")
    print(p.solve_p1())
    p = D24("d24.data")
    print(p.solve_p2(operator.add, 4))
