from utils import read_input_file, number_of_digits
from icecream import ic
from math import log10


class Stone:
    def __init__(self, number_of_digits_):
        self.number_of_digits = number_of_digits_

    def change(self) -> list:
        if int(self.number_of_digits) == 1:
            return [self]
        elif self.number_of_digits % 2 == 0:
            new_stone = Stone(self.number_of_digits // 2)
            self.number_of_digits = self.number_of_digits // 2
            return [self, new_stone]
        else:
            self.number_of_digits = self.number_of_digits + 3
            return [self]

    def __str__(self):
        return str(self.number_of_digits)


class Stones:
    def __init__(self, data: str):
        self.stones: list[Stone] = []
        for stone in data.split(' '):
            self.stones.append(Stone(number_of_digits(int(stone))))

    def blink(self):
        new_stones = []
        for stone in self.stones:
            new_stones += stone.change()
        self.stones = new_stones

    def __len__(self):
        return len(self.stones)


def main():
    data = read_input_file(file_name='example', as_one_line=True)
    print(data)
    # ic(first(data, 25))
    ic(second(data))


def first(data: str, times: int) -> int:
    stones = Stones(data)
    for i in range(0, times):
        print(i)
        stones.blink()
        print(f'length {len(stones)}')
    return len(stones)

def second(data: str) -> int:
    sum_ = 0
    for number in data.split():
        print(f'processing stone {number}')
        stones = Stones(number)
        for i in range(0, 75):
            print(i)
            stones.blink()
        sum_ += len(stones)
    return sum_


if __name__ == '__main__':
    main()
