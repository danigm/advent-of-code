import math
from base import Problem


example = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def test_d5():
    p = D5(example)
    assert p.seeds == [79, 14, 55, 13]
    assert p.maps[0].src == "seed"
    assert p.maps[0].dst == "soil"
    assert p.maps[0][98] == 50
    assert p.maps[0][99] == 51
    assert p.maps[0][96] == 98
    assert p.maps[0][52] == 54

    assert len(p.maps) == 7
    assert p.maps[4].src == "light"
    assert len(p.maps[4].ranges) == 3

    assert p.maps[0][0] == 0
    assert p.maps[0][49] == 49

    assert p.maps[0][p.seeds[0]] == 81
    assert p.track_seed(p.seeds[0]) == [79, 81, 81, 81, 74, 78, 78, 82]

    assert p.solve_p1() == 35
    assert p.solve_p2() == 46


class MapRange:
    def __init__(self, line=None):
        self.srci = 0
        self.dsti = 0
        self.length = 0
        self.offset = 0

        if line:
            dst, src, length = line.split()
            self.srci = int(src)
            self.dsti = int(dst)
            self.length = int(length)
            self.offset = self.dsti - self.srci

    def __contains__(self, key):
        return self.srci <= key < self.srci + self.length

    def __getitem__(self, key):
        return key + self.offset

    def __repr__(self):
        src = (self.srci, self.srci + self.length)
        dst = (self.dsti, self.dsti + self.length)
        return f"src: [{src}), dst: [{dst})"


class Map:
    def __init__(self, head=None):
        self.head = head
        self.src = ""
        self.dst = ""
        self.ranges = []

        if head:
            n, _ = head.split()
            self.src, _, self.dst = n.split("-")

    def add_range(self, line):
        self.ranges.append(MapRange(line))

    def range(self, key):
        for r in self.ranges:
            if key in r:
                return r
        return None

    def __getitem__(self, key):
        for r in self.ranges:
            if key in r:
                return r[key]
        return key

    def __contains__(self, key):
        for r in self.ranges:
            if key in r:
                return True
        return False

    def __repr__(self):
        return f"{self.src} -> {self.dst}: {self.ranges}"


class D5(Problem):
    def solve_p1(self):
        return min(self.track_seed(i)[-1] for i in self.seeds)

    def solve_p2(self):
        ranges = self.seed_ranges()
        current = None
        for (start, length) in ranges:
            end = start + length - 1
            x = self.min_in_map(0, (start, end))
            if not current or x < current:
                current = x

        return current

    def min_in_map(self, mapi, range, current=None):
        """
        Recursively split the range to check into small ranges that
        are in the same MapRange.

        * If the range is contained in just one MapRange, just get the
          new range index and go down to the next Map.
        * If the ranges differ, split the range in two, one with the
          start (or end element if range1 is None) and do it
          recursivelly with the rest.
        * The end condition is when we reach the last Map
          (humidity-to-location) and "start" and "end" are in the same
          range, so the minimum location is the value of "start".

        The current value is a minimum to carry for recursive calls of
        the same Map during the range split.
        """

        start, end = range
        m = self.maps[mapi]
        range1 = m.range(start)
        range2 = m.range(end)

        new_s = start
        new_e = end

        # both in the same range so new range is start, end
        if range1 == range2:
            new_s = m[start]
            new_e = m[end]
        # "start" is not in any range, so we try again with "start" ->
        # start of the range that contains "end".
        # And go ahead with start of the range that contains "end" -> "end".
        elif range1 is None:
            new_e = m[end]
            rest = range2.srci
            new_s = m[rest]
            min1 = self.min_in_map(mapi, (start, rest - 1), current)
            if not current or min1 < current:
                current = min1
        # "start" and "end" are in different ranges, so we try again with
        # end of the range that contains "start" -> "end".
        # And go ahead with "start" -> end of range that contains "start".
        else:
            new_s = m[start]
            rest = range1.srci + range1.length - 1
            new_e = m[rest]
            min1 = self.min_in_map(mapi, (rest + 1, end), current)
            if not current or min1 < current:
                current = min1

        # this is the last one, so the minium is the value of the
        # start or the carried minimum value
        if mapi == len(self.maps) - 1:
            if current is None:
                current = math.inf
            return min((new_s, current))

        return self.min_in_map(mapi + 1, (new_s, new_e), current)

    def parseinput(self, lines):
        data = super().parseinput(lines)

        self.seeds = []
        self.maps = []

        _, seeds = data[0].split(":")
        self.seeds = [int(i) for i in seeds.split()]

        map = None
        for line in data[1:]:
            # new map
            if ":" in line:
                map = Map(line)
                self.maps.append(map)
                continue

            if line and map:
                map.add_range(line)

        return data

    def seed_ranges(self):
        ranges = []
        for i in range(0, len(self.seeds), 2):
            start, length = self.seeds[i:i + 2]
            ranges.append((start, length))

        return ranges

    def track_seed(self, seed):
        values = [seed]
        current = seed
        for map in self.maps:
            current = map[current]
            values.append(current)

        return values


if __name__ == "__main__":
    print("Day 5: If You Give A Seed A Fertilizer")

    p = D5("d5.data")
    print(p.solve_p1())
    print(p.solve_p2())
