from base import Problem


example = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


def test_d4():
    c1 = Card("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert c1.points() == 8
    c2 = Card("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19")
    assert c2.points() == 2

    p = D4(example)
    assert p.solve_p1() == 13

    assert c1.range() == (2, 6)
    assert c2.range() == (3, 5)
    assert p.solve_p2() == 30


class Card:
    def __init__(self, line):
        self.number = 0
        self.winning = []
        self.numbers = []

        card, numbers = line.split(":")
        winning, numbers = numbers.split("|")
        _, n = card.split()

        self.number = int(n)
        self.winning = {int(i) for i in winning.split()}
        self.numbers = {int(i) for i in numbers.split()}

    def points(self):
        numbers = self.winning & self.numbers
        if not numbers:
            return 0

        power = len(numbers)  - 1
        return 2 ** power

    def n(self):
        return len(self.winning & self.numbers)

    def range(self):
        start = self.number + 1
        end = start + self.n()
        return start, end

    def __repr__(self):
        return self.number


class D4(Problem):
    def solve_p1(self):
        return sum(c.points() for c in self.data)

    def solve_p2(self):
        copies = {}
        for c in self.data:
            n = copies.get(c.number, 0)
            copies_of_c = n + 1
            copies[c.number] = copies_of_c
            to_copy = self.copies(c)
            for i in to_copy:
                n = copies.get(i.number, 0)
                copies[i.number] = n + copies_of_c

        return sum(i for i in copies.values())

    def copies(self, card):
        start, end = card.range()
        return self.data[start - 1:end - 1]

    def parseinput(self, lines):
        return [Card(i.strip()) for i in lines if i.strip()]


if __name__ == "__main__":
    print("Day 4: Scratchcards")

    p = D4("d4.data")
    print(p.solve_p1())
    print(p.solve_p2())
