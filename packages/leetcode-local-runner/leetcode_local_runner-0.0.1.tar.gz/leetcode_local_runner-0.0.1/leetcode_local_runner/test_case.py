from typing import Any, Dict

import numpy as np

from leetcode_local_runner.constants import PASSED, FAILED


class TestCase:
    def __init__(self, test_case: Dict, expected_output: Any) -> None:
        self.input = test_case
        self.expected_output = expected_output

    def compare(self, output, strict=False):
        if strict:
            if output == self.expected_output:
                return PASSED
            return FAILED
        else:
            if isinstance(self.expected_output, list):
                is_same = self.compare_lists(output=output)
                return PASSED if is_same else FAILED
            elif isinstance(self.expected_output, tuple):
                is_same = self.compare_tuples(output=output)
                return PASSED if is_same else FAILED
            elif isinstance(self.expected_output, str):
                return PASSED if self.expected_output == output else FAILED
            else:
                return PASSED if self.expected_output == output else FAILED

    def compare_lists(self, output, strict=False):
        if isinstance(self.expected_output[0], list):
            # It's a list of lists
            return np.array_equal(np.array(output), np.array(self.expected_output))
        else:
            if strict is False:
                expected_op_set = set(self.expected_output)
                program_op_set = set(output)
                return expected_op_set == program_op_set
            return self.expected_output == output

    def compare_tuples(self, output, strict=False):
        if strict is False:
            # We have to assume strict=False
            expected_op_set = set(self.expected_output)
            program_op_set = set(output)
            return expected_op_set == program_op_set
        return self.expected_output == output
