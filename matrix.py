from icecream import ic

def submatrix(in_matrix: list[[]], size: int, start_index: int, end_index: int, row: int) -> list[[]]:
    """ Creates a sub matrix of size extra items around the center (x, y) """
    start_column: int = start_index - size if start_index >= size else 0
    end_column: int = end_index + size if end_index + size < len(in_matrix[row]) else len(in_matrix[row])
    start_row: int = row - size if row >= size + 1 else 0
    end_row: int = row + size if row + size < len(in_matrix) else len(in_matrix)
    ic.disable()
    ic(start_column, end_column, start_row, end_row)
    ic.enable()
    sub_matrix = [a_row[start_column:end_column + 1] for a_row in in_matrix[start_row:end_row + 1]]
    return sub_matrix


def submatrix_from(in_matrix: list[[]], size: int, x: int, y: int) -> list[[]]:
    """ Creates a sub matrix of size with top left corner at x, y """
    start_x = x
    end_x = x + size if x + size <= len(in_matrix[y]) else len(in_matrix[y])
    start_y = y
    end_y = y + size if y + size <= len(in_matrix) else len(in_matrix)
    sub_matrix = [a_row[start_x:end_x] for a_row in in_matrix[start_y:end_y]]
    return sub_matrix


def get_column(matrix, column_number:int):
    column = []
    for row in matrix:
        try:
            column.append(row[column_number])
        except IndexError:
            break
    return column

def get_diagonals(matrix):
    """ returns a tuple of up_down and down_up"""
    if len(matrix) != len(matrix[0]):
        return []
    up_down = []
    size = len(matrix) - 1
    for index in range(0, len(matrix)):
        up_down.append(matrix[index][index])
    down_up = []
    for index in range(0, len(matrix)):
        down_up.append(matrix[size - index][index])
    return up_down, down_up


def print_matrix(matrix):
    """ Prints the values of the matrix. """
    for row in matrix:
        for column in row:
            print(str(column), end='')
        print()
    print()