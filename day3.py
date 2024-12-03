from icecream import ic
from utils import read_input_file
from re import compile
from enum import Enum


mul_reg = compile('mul\(\\d+,\\d+\)')
part_2_regex = compile("(mul\(\d+,\d+\))|(do\(\))|(don't\(\))")


class Type(Enum):
    MUL = 'mul'
    DO = 'do'
    DONT = "don't"


class Instruction:
    def __init__(self, type_):
        self.type = type_


class Do(Instruction):
    def __init__(self):
        super().__init__(Type.DO)


class Dont(Instruction):
    def __init__(self):
        super().__init__(Type.DONT)

class Multiplication(Instruction):
    def __init__(self, instruction):
        super().__init__(Type.MUL)
        temp = instruction[4:]
        temp = temp[:-1]
        temp = temp.split(',')
        (self.first, self.second) = temp

    def product(self):
        return int(self.first) * int(self.second)


class Engine:
    def __init__(self, instructions: [Instruction]):
        self.instructions = instructions
        self.active = True

    def process(self) -> int:
        sum_ = 0
        for instruction in self.instructions:
            if instruction.type is Type.DO:
                self.active = True
            if instruction.type is Type.DONT:
                self.active = False
            if instruction.type is Type.MUL and self.active:
                sum_ += instruction.product()
        return sum_


class Instructions:
    def __init__(self, data):
        self.instructions = self._parse_data(data)

    @staticmethod
    def _parse_data(data):
        instructions = mul_reg.findall(data)
        return [Multiplication(instruction) for instruction in instructions]


def main():
    data = read_input_file(file_name='day3', as_one_line=True)
    ic(first(data))
    ic(second(data))


def first(data) -> int:
    instructions = Instructions(data)
    result = 0
    for instruction in instructions.instructions:
        result += instruction.product()
    return result


def second(data) -> int:
    instructions = parse_instructions(data)
    engine = Engine(instructions)
    return engine.process()


def parse_instructions(data) -> [Instruction]:
    instruction_tokens = part_2_regex.findall(data)
    instructions = []
    for instruction_token in instruction_tokens:
        if instruction_token[0]:
            instructions.append(Multiplication(instruction_token[0]))
        elif instruction_token[1]:
            instructions.append(Do())
        elif instruction_token[2]:
            instructions.append(Dont())
        else:
            ic('UNKNOWN TOKEN', instruction_token)
    return instructions


if __name__ == '__main__':
    main()