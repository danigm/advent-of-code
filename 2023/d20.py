from collections import defaultdict
from base import Problem


example = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""


example2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def test_part1():
    p = D20(example)

    p = D20(example2)
    assert p.button(1) == 16
    p = D20(example2)
    assert p.button(1000) == 11687500

    p = D20(example)
    assert p.solve_p1() == 32000000

    p = D20(example2)
    assert p.solve_p1() == 11687500


def test_part2():
    p = D20(example)
    assert p.solve_p2() == 0


Hight = 1
Low = 0


class Module:
    def __init__(self, name, dests):
        self.destinations = dests
        self.name = name
        self.history = [0, 0]

    def send(self, kind, mods):
        nexts = []
        # low or high pulse
        for m in self.destinations:
            # print(self.name, "-", kind, "->", m)
            self.history[kind] += 1
            if not m in mods:
                continue
            s = mods[m].pulse(kind, self.name)
            nexts.append((m, s))

        return nexts

    def pulse(self, kind, mod):
        return 0


class FlipFlop(Module):
    prefix = "%"
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.state = False
        self.recv = None

    def pulse(self, kind, mod):
        self.recv = kind
        if kind == Low:
            self.state = not self.state
            return Hight if self.state else Low
        return None


class Conjunction(Module):
    prefix = "&"
    def __init__(self, name, dests):
        super().__init__(name, dests)
        self.recents = defaultdict(lambda: Low)

    def pulse(self, kind, mod):
        self.recents[mod] = kind
        all_hight = all(i for i in self.recents.values())
        return Low if all_hight else Hight


class Broadcaster(Module):
    def __init__(self, dest):
        super().__init__("broadcaster", dest)

    def pulse(self, kind, mod):
        return kind


class D20(Problem):
    def solve_p1(self):
        return self.button(1000)

    def solve_p2(self):
        return 0

    def button(self, repeat):
        for i in range(repeat):
            nexts = [("button", 0)]
            while nexts:
                nn = []
                for n, s in nexts:
                    if not n in self.mods or s is None:
                        continue
                    nn += self.mods[n].send(s, self.mods)
                nexts = nn
        l, h = self.recount()
        return l * h

    def recount(self):
        history = [0, 0]
        for m in self.mods.values():
            history[0] += m.history[0]
            history[1] += m.history[1]
        return history

    def parseinput(self, lines):
        self.mods = {}

        self.mods["button"] = Module("button", ["broadcaster"])
        conjs = []
        for i in lines:
            if not i.strip():
                continue
            mod, dests = i.strip().split("->")
            dests = dests.strip().split(", ")
            mod = mod.strip()
            if mod == "broadcaster":
                self.mods[mod] = Broadcaster(dests)
            elif mod[0] == "%":
                self.mods[mod[1:]] = FlipFlop(mod[1:], dests)
            elif mod[0] == "&":
                self.mods[mod[1:]] = Conjunction(mod[1:], dests)
                conjs.append(mod[1:])
            else:
                self.mods[mod] = Module(mod, dests)

        # fill all Conjunction recents dict
        for mod in self.mods.values():
            dests = mod.destinations
            for dest in dests:
                if dest in conjs:
                    self.mods[dest].recents[mod.name] = 0

        return None


if __name__ == "__main__":
    print("Day 20: Pulse Propagation")

    p = D20("d20.data")
    print(p.solve_p1())
    print(p.solve_p2())
