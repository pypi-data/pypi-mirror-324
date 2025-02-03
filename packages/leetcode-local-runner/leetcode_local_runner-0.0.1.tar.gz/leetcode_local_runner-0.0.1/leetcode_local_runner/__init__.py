
from pkg_resources import DistributionNotFound, get_distribution

from .runner import LeetCode, TestCasesChecker
from .display import DisplayResults
from .test_case import TestCase

try:
    __version__ = get_distribution("leetcode_local_runner").version
except DistributionNotFound:
    __version__ = "(local)"