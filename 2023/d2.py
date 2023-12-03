from base import Problem


example = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def test_d2():
    p = D2(example)
    assert len(p.games) == 5
    assert len(p.games[0]) == 3
    assert len(p.games[4]) == 2

    assert p.solve_p1() == 8

    assert p.solve_p2() == 2286


class P:
    def __init__(self, line=None):
        self.red = 0
        self.green = 0
        self.blue = 0

        if line is None:
            return

        colors = ["red", "green", "blue"]
        for i in line.split(","):
            n, color = i.strip().split(" ")
            n = int(n)
            match color.strip():
                case "red":
                    self.red = n
                case "green":
                    self.green = n
                case "blue":
                    self.blue = n

    def power(self):
        return self.red * self.green * self.blue


class D2(Problem):
    def solve_p1(self):
        restriction = P("12 red, 13 green, 14 blue")
        n = 0
        for i, game in enumerate(self.games, start=1):
            if self.is_possible(game, restriction):
                n += i

        return n

    def solve_p2(self):
        n = sum(self.min_p(game) for game in self.games)
        return n

    def min_p(self, game):
        p = P()
        for s in game:
            if s.red > p.red:
                p.red = s.red
            if s.green > p.green:
                p.green = s.green
            if s.blue > p.blue:
                p.blue = s.blue

        return p.power()

    def is_possible(self, game, r):
        for s in game:
            if s.red > r.red or s.green > r.green or s.blue > r.blue:
                return False

        return True

    def parse_game(self, game):
        _n, subsets = game.split(":")

        sets = []
        for subset in subsets.split(";"):
            s = P(subset)
            sets.append(s)

        return sets

    def parseinput(self, lines):
        games = super().parseinput(lines)
        self.games = [self.parse_game(i) for i in games]


if __name__ == "__main__":
    print("Day 2: Cube conundrum")

    p = D2("d2.data")
    print(p.solve_p1())
    print(p.solve_p2())
