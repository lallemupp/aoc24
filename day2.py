from icecream import ic
from utils import read_input_file
from enum import Enum


class NumberError(Exception):
    def __init__(self):
        super().__init__()
        
        
class OrderError(Exception):
    def __init__(self):
        super().__init__()


class State(Enum):
    INC = 1
    DEC = 2
    SAME = 3
    NONE = 4

    @staticmethod
    def has_state_changed(first_state, second_state):
        return first_state != second_state and first_state != State.NONE and second_state != State.NONE

    @staticmethod
    def find_state(old_value, new_value):
        if old_value == new_value:
            return State.SAME,
        if old_value > new_value:
            return State.DEC
        if old_value < new_value:
            return State.INC


class Reports:
    def __init__(self, data: [str]):
        self.reports = [Report(line) for line in data]

    def number_of_safe_reports(self, with_dampener):
        number = 0
        for report in self.reports:
            number += 1 if report.is_safe(with_dampener) else 0
        return number



def fix_report_order(report:[int], times=0):
    old_state = State.NONE
    old = report[0]
    for index, number in enumerate(report[1:]):
        current_state = State.find_state(old, number)
        if State.has_state_changed(old_state, current_state):
            if times == 0:
                del report[index]
                return fix_report_order(report, 1)
            else:
                raise OrderError
        old_state = current_state
        old = number
    return report, times


def check_order(report: [int]) -> bool:
    old_state = State.NONE
    old = report[0]
    for index, number in enumerate(report[1:]):
        current_state = State.find_state(old, number)
        if State.has_state_changed(old_state, current_state):
            return False
        old_state = current_state
        old = number
    return True


def check_numbers(report: [int]) -> bool:
    old_number = report[0]
    for index, number in enumerate(report[1:]):
        diff = abs(old_number - number)
        if diff < 1 or diff > 3:
            return False
        old_number = number
    return True


def ___check_numbers(report:[int], times=0):
    old_number = report[0]
    for index, number in enumerate(report[1:]):
        diff = abs(old_number - number)
        if diff < 1 or diff > 3:
            if times == 0:
                ic('before', report)
                if index == (len(report) - 2):
                    del report[len(report) - 1]
                else:
                    del report[index]
                ic('after', report)
                return check_numbers(report, 1)
            else:
                ic('report could not be fixed, raising error', report)
                raise NumberError


        old_number = number
    ic('safe report', report)
    return True


class Report:
    def __init__(self, report:str, with_dampener=False):
        self.report = [int(number) for number in report.split()]

    def is_safe(self, with_dampener: bool) -> bool:
        if check_numbers(self.report) and check_order(self.report):
            return True
        elif with_dampener:
            for index, _ in enumerate(self.report):
                clone = self.report.copy()
                del clone[index]
                if check_numbers(clone) and check_order(clone):
                    return True
        return False


    # def is_safe(self, with_dampener=False) -> bool:
    #     try:
    #         times = self._ordered(with_dampener)
    #     except OrderError:
    #         return False
    #     numbers_ok = self._numbers_are_ok(times)
    #     return numbers_ok
    #
    # def _ordered(self, with_dampener: bool) -> int:
    #     ic.enable()
    #     resulting_report, time = fix_report_order(self.report)
    #     self.report = resulting_report
    #     return time
    #
    # def _numbers_are_ok(self, times=0) -> bool:
    #     try:
    #         return check_numbers(self.report, times)
    #     except NumberError:
    #         return False



def main():
    data = read_input_file(file_name="day2", remove_blank_lines=True)
    reports = Reports(data)
    first_result = first(reports)
    ic("first result", first_result)
    second_result = second(reports)
    ic.enable()
    ic("second result", second_result)


def first(reports):
    return reports.number_of_safe_reports(False)

def second(reports):
    return reports.number_of_safe_reports(True)

if __name__ == '__main__':
    main()

# part 1: 534
# part 2: 577