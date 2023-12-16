from base import Problem


example = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


def test_part1():
    p = D15(example)
    assert hash("HASH") == 52
    assert hash("rn=1") == 30
    assert p.solve_p1() == 1320


def test_part2():
    p = D15(example)
    assert hash("rn") == 0
    assert hash("qp") == 1

    assert p.solve_p2() == 145


def hash(line):
    v = 0
    for i in line:
        n = ord(i)
        v = ((v + n) * 17) % 256

    return v


class Lens:
    def __init__(self, tag, focal):
        self.tag = tag
        self.focal = focal

    def __eq__(self, other):
        return self.tag == other.tag

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"[{self.tag} {self.focal}]"


class D15(Problem):
    def solve_p1(self):
        return sum(hash(i) for i in self.data)

    def solve_p2(self):
        self.hashmap()
        n = 0
        for i, box in enumerate(self.boxes):
            for j, lens in enumerate(box):
                n += (i + 1) * (j + 1) * lens.focal
        return n

    def split(self, line):
        number = 0
        symbol = "-"
        if "-" in line:
            tag = line[:-1]
        else:
            tag, number = line.split("=")
            symbol = "="

        return hash(tag), tag, symbol, int(number)

    def hashmap(self):
        for i in self.data:
            boxn, tag, symbol, n = self.split(i)
            lens = Lens(tag, n)
            box = self.boxes[boxn]
            if symbol == "-":
                # remove the tag lens from the box, and shift the rest
                if lens in box:
                    box.remove(lens)
            else:
                # if there's lens, replace old lens with new
                try:
                    index = box.index(lens)
                    box[index] = lens
                except ValueError:
                    # if no lens, add at the end
                    box.append(lens)

    def focusing_power(self, lens):
        boxn = hash(lens.tag)
        box = self.boxes[boxn]
        pos = box.index(lens) + 1
        return (boxn + 1) * pos * lens.focal

    def parseinput(self, lines):
        lines = super().parseinput(lines)
        data = lines[0].strip()
        data = data.split(",")
        self.boxes = [list() for i in range(256)]
        return data


if __name__ == "__main__":
    print("Day 15: Lens Library")

    p = D15("d15.data")
    print(p.solve_p1())
    print(p.solve_p2())
