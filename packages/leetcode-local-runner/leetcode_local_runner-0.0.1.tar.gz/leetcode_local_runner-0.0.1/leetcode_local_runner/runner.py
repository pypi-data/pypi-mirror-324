from typing import Any, Dict, List, Callable

import numpy as np

from leetcode_local_runner.constants import PASSED
from leetcode_local_runner.test_case import TestCase
from leetcode_local_runner.display import DisplayResults


class TestCasesChecker:
    def __init__(self, test_cases, expected_outputs) -> None:
        self.tests = []
        self.add_test_cases(test_cases=test_cases,
                            expected_outputs=expected_outputs)
        # list containing tuples of the form: (Passed or Failed, Input, Expected Output, Submission Output)
        self.outputs = []

    def add_test_cases(self, test_cases, expected_outputs):
        for (t, o) in zip(test_cases, expected_outputs):
            test_case = TestCase(test_case=t, expected_output=o)
            self.tests.append(test_case)

    def add_new_test_case(self, test_case, expected_output):
        test = TestCase(test_case=test_case, expected_output=expected_output)
        self.tests.append(test)

    def check_code_against_test_cases(self, tests: List[TestCase], fn: Callable, strict_checking=False):
        self.outputs = []
        for i in range(len(tests)):
            test = tests[i]
            output = fn(**test.input)
            result = test.compare(output, strict=strict_checking)
            self.outputs.append([result, test.input, test.expected_output, output])

    def run_test_cases(self, fn, strict_checking=False):
        self.check_code_against_test_cases(
            tests=self.tests, fn=fn, strict_checking=strict_checking)
        return self.outputs


class LeetCode:
    def __init__(self, test_cases: List[Dict], expected_outputs: List[Any], fn: Callable, strict_checking: bool = False):
        self.test_cases = test_cases
        self.expected_outputs = expected_outputs
        self.strict_checking = strict_checking
        self.fn = fn
        self.dr = None

    def run_test_cases(self):
        self.dr = self._run_all_test_cases()
        print(self.dr)
        all_passed = self.dr.check_all_passed()
        if all_passed is True:
            print(self.dr.message_all_passed())

    def _run_all_test_cases(self) -> DisplayResults:
        tests_runner = TestCasesChecker(
            test_cases=self.test_cases, expected_outputs=self.expected_outputs)
        # strict_checking is True because the order of values within the list matters.
        results = tests_runner.run_test_cases(
            fn=self.fn, strict_checking=self.strict_checking)

        dr = DisplayResults(results=results)
        return dr
