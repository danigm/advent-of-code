from base import Problem


example = '''
30373
25512
65332
33549
35390
'''


class D8(Problem):
    '''
    >>> p1 = D8(example)
    >>> p1.solve_p1()
    21

    >>> p1.solve_p2()
    8
    '''

    def visible_distance(self, x, y):
        current = self.data[x][y]

        # to the left
        left = 0
        for i in range(x - 1, -1, -1):
            left += 1
            if self.data[i][y] >= current:
                break

        # to the right
        right = 0
        for i in range(x + 1, len(self.data)):
            right += 1
            if self.data[i][y] >= current:
                break

        # to the top
        top = 0
        for i in range(y - 1, -1, -1):
            top += 1
            if self.data[x][i] >= current:
                break

        # to the bottom
        bottom = 0
        for i in range(y + 1, len(self.data[0])):
            bottom += 1
            if self.data[x][i] >= current:
                break

        return left * right * top * bottom

    def is_visible(self, x, y):
        if x == 0 or y == 0:
            return True
        if x == len(self.data) - 1 or y == len(self.data[0]) - 1:
            return True

        current = self.data[x][y]

        # to the left
        left = True
        for i in range(0, x):
            if self.data[i][y] >= current:
                left = False
                break

        # to the right
        right = True
        for i in range(x + 1, len(self.data)):
            if self.data[i][y] >= current:
                right = False
                break

        # to the top
        top = True
        for i in range(0, y):
            if self.data[x][i] >= current:
                top = False
                break

        # to the bottom
        bottom = True
        for i in range(y + 1, len(self.data[0])):
            if self.data[x][i] >= current:
                bottom = False
                break

        return any([left, right, top, bottom])

    def solve_p1(self):
        for i in range(len(self.data)):
            line = self.data[i]
            self.data[i] = [int(i) for i in line]

        visibles = 0

        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                is_visible = self.is_visible(i, j)
                if is_visible:
                    visibles += 1

        return visibles

    def solve_p2(self):
        max = 0
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                d = self.visible_distance(i, j)
                if d > max:
                    max = d

        return max


if __name__ == '__main__':
    p = D8('d8.input')
    print(p.solve_p1())
    print(p.solve_p2())
