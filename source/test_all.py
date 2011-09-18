"""
A module which runs all unit tests in the tests folder.

Usage: "python -m attest" or "python test_all.py"
Also supports coverage.py by "python -m coverage run -m attest"
"""
from attest import Tests, reporters
import cparser


def run():
    """Run all the tests!"""
    all_tests = Tests("tests")
    all_tests.run(reporters.PlainReporter())


if __name__ == '__main__':
    run()

