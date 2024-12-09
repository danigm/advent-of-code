from base import Problem


example = """
2333133121414131402
"""


def test_part1():
    p = D09(example)
    assert p.solve_p1() == 1928


def test_part2():
    p = D09(example)
    assert p.solve_p2() == 2858


class D09(Problem):
    def solve_p1(self):
        total = 0
        # ignore initial data as it's zero
        i, j = 0, len(self.data) - 1
        idx = int(self.data[i])
        i = 1
        end = None
        # Feeling free space with latest files chunks:
        while i < j:
            free = int(self.data[i])
            if end is None:
                end = int(self.data[j])
            while free and i < j:
                id_ = j // 2
                total += idx * id_
                end -= 1
                idx += 1
                free -= 1
                if end == 0:
                    j -= 2
                    end = int(self.data[j])
            # Add next file
            i += 1
            if i > j:
                break
            if i == j and end:
                remaining = end
            else:
                remaining = int(self.data[i])
            id_ = i // 2
            for _ in range(remaining):
                total += idx * id_
                idx += 1

            i += 1

        return total

    def solve_p2(self):
        frees = []
        files = {}
        pos = 0
        for i in range(0, len(self.data), 2):
            n = int(self.data[i])
            files[i//2] = (pos, n)
            pos += n

            try:
                free = int(self.data[i+1])
                frees.append((pos, free))
                pos += free
            except IndexError:
                pass

        for fid in reversed(files.keys()):
            pos, n = files[fid]
            for (i, (fpos, free)) in enumerate(frees):
                if fpos > pos:
                    break

                diff = free - n
                if diff < 0:
                    continue
                # move file!
                files[fid] = (fpos, n)
                if diff == 0:
                    frees = frees[:i] + frees[i+1:]
                else:
                    frees[i] = (fpos + n, diff)
                break

        total = 0
        for (k, (p, n)) in files.items():
            for i in range(n):
                total += k * (p + i)
        return total

    def parseinput(self, lines):
        data = [i.strip() for i in lines if i.strip()]
        return data[0]


if __name__ == "__main__":
    print("Day 09: Disk Fragmenter")

    p = D09("d09.data")
    print(p.solve_p1())
    print(p.solve_p2())
