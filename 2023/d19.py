from enum import Enum
from base import Problem


example = """
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_part1():
    p = D19(example)
    assert p.solve_p1() == 19114


def test_part2():
    p = D19(example)
    assert p.solve_p2() == 0


class Part:
    def __init__(self, line):
        self.x = 0
        self.m = 0
        self.a = 0
        self.s = 0
        values = line[1:-1].split(",")
        for v in values:
            k, n = v.split("=")
            setattr(self, k, int(n))

    def rate(self):
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"x={self.x},m={self.m},a={self.a},s={self.s}"


class Workflow:
    def __init__(self, line):
        name, rule = line.split("{")
        rule = rule[:-1] # remove the }

        self.name = name
        self.rules = rule.split(",")

    def consider(self, part):
        for rule in self.rules:
            if ":" not in rule:
                return rule
            cond, workflow = rule.split(":")
            if "<" in cond:
                var, value = cond.split("<")
                value = int(value)
                if getattr(part, var) < value:
                    return workflow
            else:
                var, value = cond.split(">")
                value = int(value)
                if getattr(part, var) > value:
                    return workflow

    def __repr__(self):
        return self.name


class D19(Problem):
    def solve_p1(self):
        ar = {
            "A": [],
            "R": [],
        }
        initial = self.workflows["in"]
        for p in self.parts:
            w = initial
            while w:
                w = w.consider(p)
                if w in "AR":
                    ar[w].append(p)
                    break
                w = self.workflows[w]

        return sum(i.rate() for i in ar["A"])

    def solve_p2(self):
        # min = 1, max = 4000
        return 0

    def parseinput(self, lines):
        data = []
        parts = []
        workflows = {}

        for i in lines:
            line = i.strip()
            if not line:
                continue
            # part
            if line[0] == "{":
                parts.append(Part(line))
            # workflow
            else:
                w = Workflow(line)
                workflows[w.name] = w

        self.parts = parts
        self.workflows = workflows
        return data


if __name__ == "__main__":
    print("Day 19: Aplenty")

    p = D19("d19.data")
    print(p.solve_p1())
    print(p.solve_p2())
