import os
from io import StringIO


class Problem:
    def __init__(self, input):
        self.data = None
        self.input = input
        self.readinput()

    def readinput(self):
        if not os.path.exists(self.input):
            input = StringIO(self.input)
            self.data = self.parseinput(input.readlines())
            return

        with open(self.input) as f:
            self.data = self.parseinput(f.readlines())

    def parseinput(self, lines):
        return [i.strip() for i in lines if i.strip()]

    def solve_p1(self):
        return 0

    def solve_p2(self):
        return 0
