from icecream import ic

from utils import read_input_file


class NoHoleError(Exception):
    def __init__(self):
        pass

class Hole:
    def __init__(self, start: int=None, end: int=None, indexes=None):
        if indexes is not None:
            self.indexes = indexes
        else:
            self.indexes = list(range(start, end))

    def start(self):
        return self.indexes[0]

    def end(self):
        return self.indexes[-1]

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.indexes[0] == other.indexes[0] and self.indexes[-1] == other.indexes[-1]

    def __gt__(self, other):
        if type(other) is Hole:
            result = self.indexes[0] > other.indexes[0]
            return result

    def __str__(self):
        return f'({self.indexes[0]}, {self.indexes[-1]})'

    def __len__(self):
        return len(self.indexes)


class Engine:
    def __init__(self, parsed_data: list[str]):
        self.parsed_data = parsed_data
        self.first_free_position = self._find_next_free_position()
        self.holes: dict[int, list[Hole]] = {}
        started, at = False, 0
        for i, char in enumerate(parsed_data):
            if char == '.':
                if not started:
                    started, at = True, i
            else:
                if started:
                    hole = Hole(at, i)
                    self.holes.setdefault(len(hole), []).append(hole)
                    started = False
        for _, item in self.holes.items():
            item.sort()

    def defrag(self):
        free_position = self.first_free_position
        for i, char in enumerate(self.parsed_data[::-1]):
            reversed_pos = len(self.parsed_data) - (i + 1)
            if reversed_pos < free_position:
                break
            if char != '.':
                self.parsed_data[free_position] = char
                self.parsed_data[reversed_pos] = "."
                free_position = self._find_next_free_position(free_position)

    def defrag_keep_files(self):
        reversed_ = self.parsed_data.copy()
        while len(reversed_) > 0:
            reversed_pos = len(reversed_)
            char = reversed_.pop()
            file_size = 1
            if char != '.':
                while len(reversed_) > 0 and reversed_[-1] == char:
                    file_size += 1
                    char = reversed_.pop()
                try:
                    hole_to_fill = self._get_hole(file_size)
                    if hole_to_fill.start() > reversed_pos:
                        continue
                    for i in range(file_size):
                        self.parsed_data[hole_to_fill.indexes[i]] = char
                    new_hole_size = len(hole_to_fill) - file_size
                    if new_hole_size > 0:
                        new_hole_indexes = hole_to_fill.indexes[-(len(hole_to_fill) - file_size):]
                        new_hole = Hole(indexes=new_hole_indexes)
                        self.holes.setdefault(new_hole_size, []).append(new_hole)
                    for i in range(reversed_pos - file_size, reversed_pos):
                        self.parsed_data[i] = '.'
                except (NoHoleError, IndexError):
                    pass
        return self.parsed_data


    def _get_hole(self, size) -> Hole:
        potentials: dict[int, Hole] = {}
        for key in self.holes.keys():
            if key >= size:
                self.holes[key].sort()
                try:
                    potentials[key] = self.holes[key][0]
                except IndexError:
                    pass
        lowest_start = 1000000
        lowest_key = None
        for key, item in potentials.items():
            if item.start() < lowest_start:
                lowest_key = key
                lowest_start = item.start()
        if lowest_key is not None:
            return self.holes[lowest_key].pop(0)
        else:
            raise NoHoleError


    def _find_next_free_position(self, current_free_position: int = 0) -> int:
        for i in range(current_free_position, len(self.parsed_data)):
            if self.parsed_data[i] == '.':
                return i

    def calculate_checksum(self) -> int:
        checksum = 0
        for i, number in enumerate(self.parsed_data):
            if not number == '.':
                checksum += i * int(number)
        return checksum

def main():
    data = read_input_file(file_name='day9')
    ic(first(data))
    ic(second(data))


def parse_data(data: list[str]) -> list[str]:
    data = iter(data[0])
    parsed = []
    file = True
    file_id = 0
    while True:
        try:
            if file:
                blocks = next(data)
                parsed += [file_id] * int(blocks)
                file_id += 1
            else:
                blocks = next(data)
                parsed += ['.'] * int(blocks)
            file = not file
        except StopIteration:
            break
    return parsed

def first(data: list[str]) -> int:
    engine = Engine(parse_data(data))
    engine.defrag()
    return engine.calculate_checksum()

def second(data: list[str]):
    engine = Engine(parse_data(data))
    engine.defrag_keep_files()
    return engine.calculate_checksum()

if __name__ == '__main__':
    main()

# second: 8623978542810 too high
# second: 6422623143910 too low
# second: 6436819084274 correct