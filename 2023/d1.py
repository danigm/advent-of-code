from base import Problem


example = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

example2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


class D1(Problem):
    """
    >>> p1 = D1(example)
    >>> p1.solve_p1()
    142
    >>> p1 = D1(example2)
    >>> p1.solve_p2()
    281
    """

    def parse_line(self, line):
        """
        Build a number from a str with the combination of two digits, the first
        one that appears in the string and the last one

        >>> p1 = D1(example)
        >>> p1.parse_line("1abc2")
        12
        >>> p1.parse_line("xaasdf1abc2xcvcx")
        12
        >>> p1.parse_line("xaasdf1abcxcvcx")
        11
        """

        first = None
        last = None
        for char in line:
            if '0' <= char <= '9':
                if first is None:
                    first = char
                last = char

        return int(f"{first}{last}")

    def parse_line2(self, line):
        """
        >>> p1 = D1(example)
        >>> p1.parse_line2("two1nine")
        29
        >>> p1.parse_line2("abcone2threexyz")
        13
        >>> p1.parse_line2("eightwothree")
        83
        >>> p1.parse_line2("qd8fourvmvgmssixsix8oneightps")
        88
        """

        numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        minln = min(len(n) for n in numbers)
        maxln = max(len(n) for n in numbers)

        first = None
        last = None

        index = 0
        offset = 1
        while index < len(line):
            buffer = line[index:index + offset]

            # The end, increment the start pointer
            if index + offset > len(line):
                index += 1
                offset = 1
                continue

            # We've a real number in the string
            if offset == 1 and ('0' <= buffer[0] <= '9'):
                if first is None:
                    first = buffer[0]
                last = buffer[0]
                index += 1
                offset = 1
                continue

            # str too small
            if offset < minln:
                offset += 1
                continue

            # str too large, this is not a number anymore
            if offset > maxln:
                index += 1
                offset = 1
                continue

            # It's a number
            if buffer in numbers:
                char = str(numbers.index(buffer) + 1)
                if first is None:
                    first = char
                last = char

                index += 1
                offset = 1
                continue

            offset += 1

        return int(f"{first}{last}")

    def solve_p1(self):
        return sum(self.parse_line(d) for d in self.data)

    def solve_p2(self):
        return sum(self.parse_line2(d) for d in self.data)


if __name__ == "__main__":
    print("Day 1: Trebuchet?!")

    p = D1("d1.data")
    print(p.solve_p1())

    p = D1("d1.data")
    print(p.solve_p2())
