import math
from icecream import ic
from utils import read_input_file


class PageOrderRule:
    def __init__(self, number, print_before):
        self.number = number
        self.print_before = print_before

    @staticmethod
    def parse(line: str):
        number, print_before = line.split('|')
        return PageOrderRule(number, print_before)

    def __str__(self):
        return f'{self.number}|{self.print_before}'


class PageOrderingRules:
    def __init__(self, rules: list[PageOrderRule]):
        self.after = {}
        self.before = {}
        for rule in rules:
            try:
                self.after[rule.number].append(rule.print_before)
            except KeyError:
                self.after[rule.number] = [rule.print_before]
            try:
                self.before[rule.print_before].append(rule.number)
            except KeyError:
                self.before[rule.print_before] = [rule.number]

    def is_ok(self, page: str, rest: list[str]) -> bool:
        try:
            rule = self.after[page]
        except KeyError:
            if len(rest) == 0:
                return True
            else:
                return False
        for number in rest:
            if number not in rule:
                return False
        return True


class Engine:
    def __init__(self, rules: PageOrderingRules):
        self.rules = rules

    def verify(self, pages: list[str]) -> bool:
        return True if len(self.find_wrongly_placed_pages(pages)) == 0 else False

    def is_before(self, to_test_against: str, to_test: str):
        try:
            return to_test in self.rules.after[to_test_against]
        except KeyError:
            return False

    def find_wrongly_placed_pages(self, pages) -> list[int]:
        failing_indexes = []
        for index, page in enumerate(pages):
            if not self.rules.is_ok(page, pages[index + 1:]):
                failing_indexes.append(index)
        return failing_indexes

    def brute_force_ordering(self, pages: list[str]) -> list[str]:
        fixed = []
        for original_index, page in enumerate(pages):
            if len(fixed) == 0:
                fixed.append(page)
                continue
            for fixed_index in range(0, len(fixed) + 1):
                copy = fixed.copy()
                copy.insert(fixed_index, page)
                if self.verify(copy):
                    fixed = copy
                    continue
        return fixed


def main():
    data = read_input_file(file_name='day5', remove_blank_lines=False)
    page_ordering_rules, pages_to_update = parse_data(data)
    engine = Engine(page_ordering_rules)
    # ic(first(engine, pages_to_update))
    ic(second(engine, pages_to_update))


def parse_data(data: list[str]) -> tuple[PageOrderingRules, list[list[str]]]:
    split_index = data.index('')
    ic("split_index", split_index)
    page_ordering_rules = PageOrderingRules([PageOrderRule.parse(line) for line in data[:split_index]])
    pages_to_update_in_manuals = [pages.split(',') for pages in data[split_index + 1:]]
    return page_ordering_rules, pages_to_update_in_manuals


def first(engine: Engine, pages_to_update: list[list[str]]) -> int:
    sum_ = 0
    for pages in pages_to_update:
        if engine.verify(pages):
            ic(pages_to_update, "was verified")
            sum_ += int(pages[math.floor(len(pages) / 2)])
    return sum_


def second(engine: Engine, pages_to_update: list[list[str]]) -> int:
    result = []
    sum_ = 0
    for pages in pages_to_update:
        if not engine.verify(pages):
            fixed = engine.brute_force_ordering(pages)
            result.append(fixed)
            sum_ += int(fixed[math.floor(len(pages) / 2)])
    return sum_


if __name__ == '__main__':
    main()