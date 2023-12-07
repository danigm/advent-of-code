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
    assert Hand("4JJ67", joker=True).type == HandType.Trio
    assert Hand("QJJQQ", joker=True).type == HandType.Repoker
    assert Hand("QJJQ2", joker=True).type == HandType.Poker
    assert Hand("QJQ22", joker=True).type == HandType.FullHouse
    assert Hand("4J567", joker=True).type == HandType.Duo

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
        # [number of independent, # duos, # trios, # poker, # repoker]
        eqs = [1, 0, 0, 0, 0]
        hand = sorted(hand)
        if self.joker:
            jokers = hand.count(0)
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
            eqs[equals - 1] += 1
            equals = 1

        if eqs.pop():
            return HandType.Repoker

        if self.joker and jokers:
            # Add each joker to the best hand, if there's a trio, it's a poker,
            # if it's a duo it's a trio, etc
            #
            # Just add one to the next item in eqs array and decrease the
            # number in the current.
            for _i in range(jokers):
                for j in range(1, len(eqs) + 1):
                    if not eqs[-j]:
                        continue
                    if eqs[-j]:
                        if j == 1:
                            return HandType.Repoker
                        eqs[-j + 1] += 1
                        eqs[-j] -= 1
                        break

        if eqs[3]:
            return HandType.Poker

        if eqs[2] and eqs[1]:
            return HandType.FullHouse

        if eqs[2]:
            return HandType.Trio

        if eqs[1] == 2:
            return HandType.DoubleDuo
        if eqs[1]:
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
