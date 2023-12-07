from enum import Enum
from base import Problem


example = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def test_d7():
    p = D7(example)

    assert Hand("33332") > Hand("2AAAA")
    assert Hand("77888") > Hand("77788")

    assert p.solve_p1() == 6440
    assert str(p.rank[0]) == "32T3K"
    assert str(p.rank[-1]) == "QQQJA"


def test_d7_part2():
    assert Hand("QJJQ2", joker=True).type == HandType.Poker

    assert Hand("33332", joker=True) > Hand("2AAAA", joker=True)
    assert Hand("77888", joker=True) > Hand("77788", joker=True)
    assert Hand("JKKK2", joker=True) < Hand("QQQQ2", joker=True)
    p = D7(example, joker=True)
    assert p.solve_p1() == 5905


CARDS = "23456789TJQKA"
CARDS_JOKER = "J23456789TQKA"


class HandType(Enum):
    Repoker = 7
    Poker = 6
    FullHouse = 5
    Trio = 4
    DoubleDuo = 3
    Duo = 2
    One = 1

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value


class Hand:
    def __init__(self, hand, bid=0, joker=False):
        if joker:
            self.hand = [CARDS_JOKER.index(i) for i in hand]
        else:
            self.hand = [CARDS.index(i) for i in hand]
        self.joker = joker
        self.high = max(self.hand)
        self.type = self.calc_hand_type(self.hand)
        self.bid = bid
        self._line = hand

    def __str__(self):
        return self._line

    def __repr__(self):
        return f"{self._line} {self.type}"

    def calc_hand_type(self, hand):
        duos = 0
        trios = 0
        poker = 0
        jokers = hand.count(0)
        hand = sorted(hand)
        if self.joker:
            hand = [i for i in hand if i]
            if not hand:
                return HandType.Repoker

        equals = 1
        card = hand[0]
        for i, c in enumerate(hand[1:]):
            if c == card:
                equals += 1
                if i < len(hand[1:]) - 1:
                    continue

            card = c
            if equals == 2:
                duos += 1
            if equals == 3:
                trios += 1
            if equals == 4:
                poker += 1
            if equals == 5:
                return HandType.Repoker

            equals = 1

        if poker:
            if self.joker and jokers:
                return HandType.Repoker
            return HandType.Poker

        if trios and duos:
            return HandType.FullHouse

        if trios:
            if self.joker and jokers:
                if jokers == 2:
                    return HandType.Repoker
                return HandType.Poker
            return HandType.Trio

        if duos == 2:
            if self.joker and jokers:
                return HandType.FullHouse
            return HandType.DoubleDuo
        if duos:
            if self.joker and jokers:
                if jokers == 3:
                    return HandType.Repoker
                if jokers == 2:
                    return HandType.Poker
                return HandType.Trio
            return HandType.Duo

        if self.joker and jokers:
            if jokers == 4:
                return HandType.Repoker
            if jokers == 3:
                return HandType.Poker
            if jokers == 2:
                return HandType.Trio
            return HandType.Duo
        return HandType.One

    def __lt__(self, other):
        if self.type == other.type:
            return self.hand < other.hand
        return self.type < other.type

    def __gt__(self, other):
        if self.type == other.type:
            return self.hand > other.hand
        return self.type > other.type

    def __eq__(self, other):
        return self.hand == other.hand


class D7(Problem):
    def __init__(self, input, joker=False):
        self.joker = joker
        super().__init__(input)

    def solve_p1(self):
        self.rank = sorted(self.data)
        return sum(h.bid * i for i, h in enumerate(self.rank, 1))

    def parseinput(self, lines):
        data = []
        for i in lines:
            line = i.strip()
            if not line:
                continue
            hand, bid = line.split()
            data.append(Hand(hand, int(bid), self.joker))
        return data


if __name__ == "__main__":
    print("Day 7: Camel Cards")

    p = D7("d7.data")
    print(p.solve_p1())
    p = D7("d7.data", joker=True)
    print(p.solve_p1())
