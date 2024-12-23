from abc import abstractmethod
from itertools import product

from icecream import ic

import utils
from utils import read_input_file


class Number:
    def __init__(self, value: int):
        self.value: int = value

    def __str__(self):
        return str(self.value)


class Operation:
    @abstractmethod
    def process(self, first: int, second: int) -> int:
        pass


class Addition(Operation):
    def process(self, first: int, second: int) -> int:
        return first + second

    def __str__(self):
        return '+'

class Concatination(Operation):
    def process(self, first: int, second: int) -> int:
        return int(f'{first}{second}')

    def __str__(self):
        return '||'

class Multiplication(Operation):
    def process(self, first: int, second: int) -> int:
        return first * second

    def __str__(self):
        return '*'


class Permutation:
    def __init__(self, permutation):
        self.permutation = permutation

    def __str__(self):
        return ''.join([str(thing) for thing in self.permutation])


class Equation:
    def __init__(self, equation: str, possible_operators=2):
        self.result = int(equation.split(':')[0].strip())
        self.factors = [int(number) for number in equation.split(':')[1].split()]
        self.possible_operators = possible_operators

    def have_solution(self) -> bool:
        permutations = self.create_permutations()
        for permutation in permutations:
            if self.solve(permutation):
                return True
        return False

    def create_permutations(self):
        number_of_operators = len(self.factors) - 1
        magic_lists = list(product(range(0, self.possible_operators), repeat=number_of_operators))
        permutations = []
        for magic_list in magic_lists:
            permutation = []
            for i, factor in enumerate(self.factors):
                permutation.append(Number(factor))
                if i == len(self.factors) - 1:
                    break
                if magic_list[i] == 0:
                    permutation.append(Addition())
                elif magic_list[i] == 1:
                    permutation.append(Multiplication())
                elif magic_list[i] == 2:
                    permutation.append(Concatination())
            permutations.append(permutation)
        return permutations

    def solve(self, permutation: list) -> bool:
        result = permutation[0].value
        operation: Operation = None
        for part in permutation[1:]:
            if type(part) == Number:
                result = operation.process(result, part.value)
            else:
                operation = part
        return result == self.result

    def __str__(self):
        return f'{self.result}: {' '.join([str(factor) for factor in self.factors])}'


def main():
    data = read_input_file(file_name='day7')
    #ic(first(data, 2))
    ic(first(data, 3))


def first(data, possible_operators) -> int:
    equations = [Equation(line, possible_operators) for line in data]
    numbers = []
    for equation in equations:
        if equation.have_solution():
            ic('adding', equation.result)
            numbers.append(equation.result)
    return sum(numbers)


if __name__ == '__main__':
    ic.enable()
    main()

# part 1 416522731268 to low
# part 1 538191549061 CORRECT
# part 2 34612812972206