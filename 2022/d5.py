from base import Problem


debug = False


example = '''
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''


class D5(Problem):
    '''
    >>> p1 = D5(example)
    >>> p1.solve_p1()
    'CMZ'
    >>> p1 = D5(example)
    >>> p1.solve_p2()
    'MCD'
    '''

    def parseinput(self, lines):
        input = [i.strip('\n') for i in lines]
        if not input[0]:
            input = input[1:]

        n = input.index('')
        state = input[0:n]
        moves = input[n+1:]

        self.parsestate(state)
        self.parsemoves(moves)

    def parsestate(self, state):
        numbers = state.pop().split()
        initial = 1
        steps = 4
        stacks = [[] for i in numbers]

        for line in state:
            for i, s in enumerate(stacks):
                crate = line[initial + steps * i]
                if crate.strip():
                    s.insert(0, crate)

        self.state = stacks

    def printstate(self):
        if not debug:
            return

        lines = max(len(i) for i in self.state)
        for i in range(lines - 1, -1, -1):
            line = []
            for stack in self.state:
                if len(stack) >= i + 1:
                    crate = stack[i]
                    line.append(f'[{crate}]')
                else:
                    line.append('   ')

            print(' '.join(line))

        print(' '.join(f' {i+1} ' for i in range(len(self.state))))

    def parsemoves(self, moves):
        self.moves = []
        for i in moves:
            _move, n, _from, s1, _to, s2 = i.split()
            self.moves.append((int(n), int(s1), int(s2)))

    def domove(self, move, multiple=False):
        n, s1, s2 = move
        froms = self.state[s1 - 1]
        tos = self.state[s2 - 1]

        if multiple:
            block = froms[-n:]
            self.state[s1 - 1] = froms[:-n]
            self.state[s2 - 1] = tos + block
            return

        while n:
            tos.append(froms.pop())
            n = n - 1

    def solve_p1(self, multiple=False):
        self.printstate()
        for m in self.moves:
            self.domove(m, multiple)
            self.printstate()

        solution = [i[-1] for i in self.state]
        return ''.join(solution)

    def solve_p2(self):
        p2 = self.solve_p1(True)
        return p2


if __name__ == '__main__':
    p = D5('d5.input')
    print(p.solve_p1())

    p = D5('d5.input')
    print(p.solve_p2())
