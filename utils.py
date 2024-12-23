""" Utils """
from icecream import ic
from requests import get
from cookie import cookie


class HashableList(list):
    def __hash__(self):
        hash_ = sum([hash(value) for value in self])
        return hash_

def read_input_file(folder: str = 'data', file_name: str = 'test.txt', remove_blank_lines=True, as_one_line=False) -> list[str]:
    with open(f'{folder}/{file_name}') as file:
        data = file.readlines()
    response = [line.strip() for line in data if line.rstrip()] if remove_blank_lines else [line.strip() for line in data]
    if as_one_line:
        response = ''.join(response)
    return response


def replace_at_index(a_list, to_replace, index):
    a_list[index] = to_replace


def permute(original, new, length):
    permutations = []
    a = [original for i in range(length)]
    for i in range(len(a)):
        for j in range(i, len(a)):
            copy = a.copy()
            copy[j] = new
            permutations.append(HashableList(copy))
        a[i] = new
    return permutations


def number_of_input_lines(folder: str = 'data', file_name: str = 'test.txt') -> int:
    return len(read_input_file(folder, file_name))

def read_data_fom_online(day: int) -> list[str]:
    response = get(f'https://adventofcode.com/2024/day/{day}/input', headers={'Cookie': cookie})
    return [row for row in response.text.splitlines()]