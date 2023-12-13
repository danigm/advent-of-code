from functools import lru_cache
import pprint
import re
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

    assert set(p.possibilities2("???.###")) == set(["....###", ".#..###", "..#.###", "#...###", "###.###", "##..###", "#.#.###", ".##.###"])
    assert set(p.possibilities2(".??..??.")) == set(["........", "..#.....", ".#......",  ".##.....", ".....#..", "..#..#..", ".#...#..",  ".##..#..", ".....##.", "..#..##.", ".#...##.",  ".##..##.", "......#.", "..#...#.", ".#....#.", ".##...#."])

    assert p.possibilities("???.###", (1,1,3)) == ["#.#.###"]

    assert p.arrangements(p.springs[0]) == 1
    assert p.arrangements(p.springs[1]) == 4
    assert p.arrangements(p.springs[2]) == 1
    assert p.arrangements(p.springs[3]) == 1
    assert p.arrangements(p.springs[4]) == 4
    assert p.arrangements(p.springs[5]) == 10
    assert p.solve_p1() == 21


def test_pos():
    p = D12(example)
    assert p.arrangements((".??..??...?##.", [1,1,3])) == 4
    # s1 = p.arrangements(("???#????.#???????",[2, 1, 6]))
    # s2 = p.arrangements3(("???#????.#???????",[2, 1, 6]))
    # assert s1 == s2


def test_part2():
    p = D12(example)
    assert p.unfold(".#", [1]) == (".#?" * 4 + ".#", [1] * 5)
    assert p.unfold("???.###", [1,1,3]) == ("???.###?" * 4 + "???.###", [1,1,3] * 5)

    assert p.arrangements(("????.#...#...", [4,1,1]), False) == 1
    assert p.arrangements(("????.#...#...", [4,1,1]), True) == 16
    assert p.solve_p2() == 525152


class D12(Problem):
    def solve_p1(self):
        return sum(self.arrangements(r) for r in self.springs)

    def solve_p2(self):
        return sum(self.arrangements(r, True) for r in self.springs)

    def unfold(self, springs, correction):
        return "?".join([springs] * 5), correction * 5

    def arrangements(self, row, unfold=False):
        springs, correction = row

        if unfold:
            s, c = self.unfold(springs, correction)
            return self.npos(s, tuple(c))
        return self.npos(springs, tuple(correction))

    @lru_cache
    def npos_broken(self, springs, correction, group):
        # get the full group
        g = springs[:group]
        # Check that the group is valid, contains # or ? and it's the
        # correct size.
        if "." in g or len(g) < group:
            return 0
        # If this is the last group
        if len(springs) == group:
            # Then there should not be more groups
            return int(len(correction) == 1)

        # it should be and end of group
        if springs[group] in ".?":
            # we continue calculating recursively the next group
            return self.npos(springs[group+1:], correction[1:])

        # in other case there are more # so this doesn't match the
        # group
        return 0

    @lru_cache
    def npos(self, springs, correction):
        """
        Not my code, just copy the solution from reddit after trying
        different solutions without luck.
        https://www.reddit.com/r/adventofcode/comments/18hbbxe/2023_day_12python_stepbystep_tutorial_with_bonus/
        """

        # no more groups
        if not correction:
            return int("#" not in springs)

        # no more chars
        if not springs:
            return 0

        group = correction[0]
        char = springs[0]

        n1 = 0
        n2 = 0
        if char in ".?":
            # Calculate possibilities if this is a dot
            n1 = self.npos(springs[1:], correction)
        if char in "#?":
            # Calculate possibilities if this is a #
            n2 = self.npos_broken(springs, correction, group)

        # if the char is ? we add the two, in other case one of them
        # will be zero so just one branch.
        return n1 + n2

    def arrangements3(self, row, unfold=False):
        """
        This is the best solution that I was able to implement without
        the help of reddit, it's a recursive version, check all
        branches using regular expressions.

        Not valid to use the cache because the correction is passed
        completely so there's no repetition
        """
        springs, correction = row
        print(springs, correction, unfold)

        if unfold:
            s, c = self.unfold(springs, correction)
            return len(self.possibilities(s, tuple(c)))

        return len(self.possibilities(springs, tuple(correction)))

    @lru_cache
    def possibilities(self, springs, correction, regex=None):
        try:
            unknown = springs.index("?")
        except ValueError:
            return [springs]

        nbroken = sum(correction)
        ndots = len(springs) - nbroken
        known_dots = springs.count(".")
        known_broken = springs.count("#")
        unknown_dots = ndots - known_dots
        unknown_broken = nbroken - known_broken

        pos = []
        if regex is None:
            regex = self.get_regex(correction)

        p1 = springs[:unknown] + "." + springs[unknown + 1:]
        p2 = springs[:unknown] + "#" + springs[unknown + 1:]

        if regex.match(p1):
            pos += self.possibilities(p1, correction, regex)
        if regex.match(p2):
            pos += self.possibilities(p2, correction, regex)

        return pos

    def get_regex(self, correction):
        p1 = r"[#\?]"

        regex = r"^[\.\?]*"
        for i, c in enumerate(correction):
            regex += p1 + r"{" + str(c) + "}"
            if i == len(correction) - 1:
                regex += r"[\.\?]*$"
            else:
                regex += r"[\.\?]+"

        return re.compile(regex)

    def arrangements2(self, row):
        """
        My first attempt, do all combinations. This is too slow
        """

        springs, correction = row

        pos = self.possibilities2(springs)
        valid = [i for i in pos if self.match(i, correction)]
        print(valid)
        return len(valid)

    def possibilities2(self, springs):
        """ Use combinations to generate all possibilities """
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
    print(p.solve_p2())
