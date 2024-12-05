from base import Problem
from functools import cmp_to_key


example = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part1():
    p = D05(example)
    assert p.solve_p1() == 143


def test_part2():
    p = D05(example)
    assert p.solve_p2() == 123


class D05(Problem):
    def _cmp(self, a, b):
        if (a, b) in self.order:
            return -1
        if (b, a) in self.order:
            return 1
        return 0

    def solve_p1(self):
        """
         * Updates in the correct order
         * Add middle page number for those
        """

        n = 0
        for i in self.updates:
            s = sorted(i, key=cmp_to_key(self._cmp))
            if i == s:
                n += i[len(i) // 2]

        return n

    def solve_p2(self):

        n = 0
        for i in self.updates:
            s = sorted(i, key=cmp_to_key(self._cmp))
            if i != s:
                n += s[len(s) // 2]

        return n

    def parseinput(self, lines):
        self.order = set()
        self.updates = []
        for line in lines:
            l = line.strip()
            if not l:
                continue
            if "|" in l:
                first, second = l.split("|")
                self.order.add((int(first), int(second)))
            if "," in l:
                update = [int(i) for i in l.split(",")]
                self.updates.append(update)

        return self.order, self.updates


if __name__ == "__main__":
    print("Day 05: Print Queue")

    p = D05("d05.data")
    print(p.solve_p1())
    print(p.solve_p2())
