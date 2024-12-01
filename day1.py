from icecream import ic
from utils import read_input_file

def second(left, right):
    occurrence_map = create_occurrence_map(right)
    similarity_score = 0
    for number in left:
        occurrence = occurrence_map.get(number, 0)
        similarity_score += number * occurrence
    return similarity_score

def first(left, right):
    left.sort()
    right.sort()
    error = sum_error(left, right)
    return error

def input_to_arrays(data):
    input_with_comma = [line.replace('   ', ',') for line in data]
    left = []
    right = []
    for line in input_with_comma:
        try:
            left.append(int(line.split(',')[0]))
            right.append(int(line.split(',')[1]))
        except:
            pass
    return left, right


def create_occurrence_map(right: [int]) -> {int: int}:
    occurrence = {}
    for number in right:
        if number in occurrence:
            occurrence[number] += 1
        else:
            occurrence[number] = 1
    return occurrence


def sum_error(left: [int], right: [int]):
    error = 0
    for index in range(0, len(left)):
        left_int = left[index]
        right_int = right[index]
        diff = abs(left_int - right_int)
        error += diff
    return error

def main():
    data = read_input_file(file_name='day1', remove_blank_lines=True)
    left, right = input_to_arrays(data)
    ic(first(left, right))
    ic(second(left, right))


if __name__ == '__main__':
    main()
