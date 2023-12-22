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
        # &hb -> rx (sends 0 when all inputs are 1)
        # &js -> hb
        # &zb -> hb
        # &bs -> hb
        # &rr -> hb

        # The hb will send a 0 when all inputs sends a 1. We look for
        # the loop when each of the input modules sends a 1 and then
        # multiply all to get the loop when all sends 1 at the same
        # time.
        final_states = [("js", 1), ("zb", 1), ("bs", 1), ("rr", 1)]
        inloop = {"js": 0, "zb": 0, "bs": 0, "rr": 0}
        i = 0
        while final_states:
            i += 1
            found = self._press_button(final_states)
            for f in found:
                inloop[f] = i

        n = 1
        for m in inloop.values():
            n *= m
        return n

    def button(self, repeat):
        for i in range(repeat):
            self._press_button()

        l, h = self.recount()
        return l * h

    def _press_button(self, final_states=None):
        nexts = [("button", 0)]
        found = []
        while nexts:
            nn = []
            for n, s in nexts:
                if not n in self.mods or s is None:
                    continue
                nn += self.mods[n].send(s, self.mods)
            nexts = nn

            # part 2
            if final_states:
                for st in final_states:
                    if st in nexts:
                        final_states.remove(st)
                        found.append(st[0])

        return found

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
    p = D20("d20.data")
    print(p.solve_p2())
