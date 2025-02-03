from typing import Any, Dict, List, Callable, Text

import termcolor
import numpy as np

from leetcode_local_runner.constants import PASSED, FAILED


class DisplayResults:
    COLOR_PASSED = "#2cbb5d"
    COLOR_FAILED = "#e64541"

    BORDER = "----------------------------------------------------------------------"
    THICK_BORDER = "======================================================================"
    MINI_BORDER = "---------"

    INPUT = "Input"
    OUTPUT = "Output"
    EXPECTED = "Expected"

    def __init__(self, results: List[List[Any]]) -> None:
        self.results = results

    def display_single_result(self, result):
        output_str = ""
        passed_or_failed, given_input, expected_output, output = result
        if passed_or_failed == PASSED:
            output_str += termcolor.colored(PASSED, 'green') + "\n"
        else:
            output_str += termcolor.colored(FAILED, 'red') + "\n"
        # output_str += self.MINI_BORDER + "\n"
        output_str += self.BORDER + "\n"
        output_str += self.INPUT + ":\n"
        output_str += str(given_input) + "\n"
        output_str += self.OUTPUT + ":\n"
        output_str += str(output) + "\n"
        output_str += self.EXPECTED + ":\n"
        output_str += str(expected_output) + "\n"
        output_str += self.BORDER + "\n"
        return output_str

    def display_results(self):
        output_to_print = ''
        output_to_print += self.BORDER + "\n"
        for i in range(len(self.results)):
            result = self.results[i]
            output_to_print += self.display_single_result(result=result)
        return output_to_print
    
    def check_all_passed(self):
        results = [r[0] for r in self.results]
        
        passed = [PASSED for _ in range(len(results))]
        
        bool_results = (np.array(passed) == np.array(results)).tolist()
        return all(bool_results)
    
    @staticmethod
    def message_all_passed():
        output_str = ''
        output_str += DisplayResults.THICK_BORDER + "\n"
        output_str += termcolor.colored("All Test Cases Passed!", 'green') + "\n"
        output_str += DisplayResults.THICK_BORDER + "\n"
        return output_str

    def __str__(self) -> str:
        output_to_print = self.display_results()
        return output_to_print