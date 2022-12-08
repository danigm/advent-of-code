from base import Problem


example = '''mjqjpqmgbljsphdztnvjfqwrcgsmlb'''
e2 = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
e3 = 'nppdvjthqldpwncqszvftbrmjlhg'
e4 = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
e5 = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'


class D6(Problem):
    '''
    >>> p1 = D6(example)
    >>> p2 = D6(e2)
    >>> p3 = D6(e3)
    >>> p4 = D6(e4)
    >>> p5 = D6(e5)

    >>> p1.solve_p1()
    7
    >>> p2.solve_p1()
    5
    >>> p3.solve_p1()
    6
    >>> p4.solve_p1()
    10
    >>> p5.solve_p1()
    11

    >>> p1.solve_p2()
    19
    >>> p2.solve_p2()
    23
    >>> p3.solve_p2()
    23
    >>> p4.solve_p2()
    29
    >>> p5.solve_p2()
    26
    '''

    def solve_p1(self, n=4):
        stream = self.data[0]
        uniq = []
        for i, s in enumerate(stream):
            uniq = [s]
            for j, s1 in enumerate(stream[i+1:]):
                if s1 in uniq:
                    break
                uniq.append(s1)
                if len(uniq) == n:
                    return i + j + 2
        return 0

    def solve_p2(self):
        return self.solve_p1(14)


if __name__ == '__main__':
    p = D6('d6.input')
    print(p.solve_p1())
    print(p.solve_p2())
