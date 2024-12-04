from icecream import ic
from utils import read_input_file
from matrix import  submatrix_from, get_column, get_diagonals


class Puzzle:
    current = (0, 0)
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])

    def submatrix(self, size: int, x: int, y: int):
        return submatrix_from(self.data, size, x, y)


def is_hit(text:str, check_against='XMAS') -> bool:
    return text == check_against or text == check_against[::-1]


def main():
    input_file = 'day4'
    data = read_input_file(file_name=input_file)
    puzzle = Puzzle(data)
    ic("first", first(puzzle))
    ic("second", second(puzzle))


def first(puzzle:Puzzle) -> int:
    number_of_hits = 0
    for y in range(0, puzzle.rows):
        for x in range(0, puzzle.columns):
            sub_matrix = puzzle.submatrix(4, x, y)
            number_of_hits += find_xmas_in(sub_matrix)
    return number_of_hits


def find_xmas_in(matrix:list[str]) -> int:
    number_of_hits = check_horizontal(matrix)
    number_of_hits += check_vertically(matrix)
    number_of_hits += check_diagonals(matrix)
    return number_of_hits


def check_horizontal(matrix:list[str]) -> int:
    """ Only check the first row in the matrix since otherwise rows would be checked multiple times. """
    first_row = matrix[0]
    if is_hit(first_row):
        return 1
    else:
        return 0


def check_vertically(matrix:list[str]) -> int:
    """ Only check first column in the matrix since otherwise columns would be checked multiple times."""
    column = "".join(get_column(matrix, 0))
    if is_hit(column):
        return 1
    else:
        return 0


def check_diagonals(matrix:list[str]) -> int:
    diagonals = get_diagonals(matrix)
    number_of_hits = 0
    diagonals = [''.join(diagonal) for diagonal in diagonals]
    for diagonal in diagonals:
        if is_hit(diagonal):
            number_of_hits += 1
    return number_of_hits


def second(puzzle: Puzzle) -> int:
    number_of_hits = 0
    for y in range(0, puzzle.rows):
        for x in range(0, puzzle.columns):
            submatrix = puzzle.submatrix(3, x, y)
            number_of_hits += find_double_mas_in(submatrix)
    return number_of_hits

def find_double_mas_in(matrix: list[str]) -> int:
    if len(matrix[0]) < 3 or len(matrix) < 3:
        return 0
    if matrix[1][1] != 'A':
        return 0
    diagonals = ["".join(diagonal) for diagonal in get_diagonals(matrix)]
    double_mas = True
    for diagonal in diagonals:
        if not is_hit(diagonal, check_against="MAS"):
            double_mas = False
    return 1 if double_mas else 0



if __name__ == '__main__':
    main()

# day 1: 192 to low