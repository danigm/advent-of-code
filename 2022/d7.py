import os
from base import Problem


example = '''
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''


FILESYSTEM = 70_000_000
UPDATE = 30_000_000


class D7(Problem):
    '''
    >>> p1 = D7(example)
    >>> p1.solve_p1()
    95437

    >>> p1.solve_p2()
    24933642
    '''

    def __init__(self, input):
        self.tree = {
            '/': [],
        }
        super().__init__(input)

    def dirsize(self, d):
        s = 0
        for (size, fname) in self.tree[d]:
            if not size:
                s += self.dirsize(os.path.join(d, fname))
            s += size
        return s

    def parseinput(self, lines):
        lines = list(reversed(super().parseinput(lines)))
        self.parselines(lines)

    def parselines(self, lines, dir=''):
        while lines:
            line = lines.pop()
            if line.startswith('$ cd'):
                _, _cd, dst = line.split()
                if dst == '..':
                    return
                dst = os.path.join(dir, dst)
                if not dst in self.tree:
                    self.tree[dst] = []
                self.parselines(lines, dst)
                continue

            if line == '$ ls':
                continue

            if line.startswith('dir'):
                _dir, filename = line.split()
                size = 0
            else:
                size, filename = line.split()
                size = int(size)

            self.tree[dir].append((size, filename))

    def solve_p1(self):
        total = 0
        for k in self.tree:
            size = self.dirsize(k)
            if size <= 100000:
                total += size
        return total

    def solve_p2(self):
        to_delete = []
        root = self.dirsize('/')
        for k in self.tree:
            size = self.dirsize(k)
            if FILESYSTEM - (root - size) >= UPDATE:
                to_delete.append(size)
        return min(to_delete)


if __name__ == '__main__':
    p = D7('d7.input')
    print(p.solve_p1())
    print(p.solve_p2())
