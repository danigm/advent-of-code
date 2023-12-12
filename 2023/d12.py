import itertools
from base import Problem


example = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""


def test_part1():
    p = D12(example)
    assert p.match("#.#.###", [1,1,3])
    assert not p.match("#...###", [1,1,3])
    assert not p.match("##..###", [1,1,3])
    assert not p.match("#.#.#.#", [1,1,3])
    assert not p.match("#.#.###.#", [1,1,3])

    assert set(p.possibilities("???.###")) == set(["....###", ".#..###", "..#.###", "#...###", "###.###", "##..###", "#.#.###", ".##.###"])
    assert set(p.possibilities(".??..??.")) == set(["........", "..#.....", ".#......",  ".##.....", ".....#..", "..#..#..", ".#...#..",  ".##..#..", ".....##.", "..#..##.", ".#...##.",  ".##..##.", "......#.", "..#...#.", ".#....#.", ".##...#."])

    assert p.arrangements(p.springs[0]) == 1
    assert p.arrangements(p.springs[1]) == 4
    assert p.arrangements(p.springs[2]) == 1
    assert p.arrangements(p.springs[3]) == 1
    assert p.arrangements(p.springs[4]) == 4
    assert p.arrangements(p.springs[5]) == 10
    assert p.solve_p1() == 21


def test_part2():
    p = D12(example)
    assert p.solve_p2() == 0


class D12(Problem):
    def solve_p1(self):
        return sum(self.arrangements(r) for r in self.springs)

    def solve_p2(self):
        return 0

    def arrangements(self, row):
        springs, correction = row

        pos = self.possibilities(springs)
        valid = [i for i in pos if self.match(i, correction)]
        return len(valid)

    def possibilities2(self, springs, correction):
        groups = [i for i in springs.split(".") if i]
        if len(groups) == len(correction):
            # TODO: do combinations in groups with "?"
            pass
        else:
            # TODO: Try to split big groups using the correction
            # numbers
            pass

        return []

    def possibilities(self, springs):
        p = []

        unknowns = []
        for i, s in enumerate(springs):
            if s == "?":
                unknowns.append(i)

        n = len(unknowns)
        perms = set(itertools.combinations(".#" * n, n))

        for x in perms:
            options = list(x)
            perm = list(springs)
            for i, s in enumerate(springs):
                if s == "?":
                    perm[i] = options.pop(0)
            p.append("".join(perm))

        return p

    def match(self, springs, correction):
        # copy the array to modify it
        cs = [c for c in correction]
        csi = 0
        prev = None
        for i in springs:
            if i == "#" and csi >= len(cs):
                return False

            if i == ".":
                if prev == "#":
                    csi += 1
            elif i == "#":
                cs[csi] -= 1
            prev = i

        return not bool([i for i in cs if i != 0])

    def parseinput(self, lines):
        data = super().parseinput(lines)
        self.springs = []

        for line in data:
            d, correction = line.split()
            correction = [int(i) for i in correction.split(",")]
            self.springs.append((d, correction))
        return data


if __name__ == "__main__":
    print("Day 12: Hot Springs")

    p = D12("d12.data")
    print(p.solve_p1())
    p = D12("d12.data")
    print(p.solve_p2())
