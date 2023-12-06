from base import Problem


example = """
Time:      7  15   30
Distance:  9  40  200
"""

def test_d6():
    p = D6(example)
    assert p.times == [7, 15, 30]
    assert p.distances == [9, 40, 200]
    assert p.races[0] == (7, 9)

    assert p.distance(7, 0) == 0
    assert p.distance(7, 1) == 6
    assert p.distance(7, 2) == 10
    assert p.distance(7, 3) == 12
    assert p.distance(7, 4) == 12
    assert p.distance(7, 5) == 10
    assert p.distance(7, 6) == 6
    assert p.distance(7, 7) == 0

    assert p.nwins(7, 9) == 4
    assert p.nwins(15, 40) == 8
    assert p.nwins(30, 200) == 9

    assert p.solve_p1() == 288
    assert p.solve_p2() == 71503


class D6(Problem):
    def solve_p1(self):
        r = 1
        for (time, record) in self.races:
            nwins = self.nwins(time, record)
            r = r * nwins
        return r

    def solve_p2(self):
        time, record = self.big_race
        return self.nwins(time, record)

    def parseinput(self, lines):
        data = super().parseinput(lines)

        self.times = [int(i) for i in data[0].split(":")[1].split()]
        self.distances = [int(i) for i in data[1].split(":")[1].split()]
        self.races = list(zip(self.times, self.distances))

        self.big_race = (int("".join(str(i) for i in self.times)),
                         int("".join(str(i) for i in self.distances)))

        return data

    def distance(self, time, hold):
        return hold * (time - hold)

    def nwins(self, time, record):
        min_win = 1
        for i in range(1, time // 2):
            if self.distance(time, i) > record:
                min_win = i
                break

        return (time - min_win) - min_win + 1


if __name__ == "__main__":
    print("Day 6: Wait For It")

    p = D6("d6.data")
    print(p.solve_p1())
    print(p.solve_p2())
