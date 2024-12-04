""" Utils """
from icecream import ic

def read_input_file(folder: str = 'data', file_name: str = 'test.txt', remove_blank_lines=True, as_one_line=False) -> [str]:
    with open(f'{folder}/{file_name}') as file:
        data = file.readlines()
    response = [line.strip() for line in data if line.rstrip()] if remove_blank_lines else [line.strip() for line in data]
    if as_one_line:
        response = ''.join(response)
    return response


def number_of_input_lines(folder: str = 'data', file_name: str = 'test.txt') -> int:
    return len(read_input_file(folder, file_name))



