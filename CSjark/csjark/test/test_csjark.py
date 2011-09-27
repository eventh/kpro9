"""
Module for testing the csjark module. Especially command line interface.
"""

import sys, os
from attest import Tests, assert_hook

try:
    import cparser
except ImportError:
    # If cparser is not installed, look in parent folder
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))
    import cparser

cli = Tests()

@cli.test
def cli_test_header():
    assert False

@cli.test
def cli_test_flag():
    """Test that the commandline interface flags are working"""
    assert True


if __name__ == '__main__':
    all_tests = Tests([cli])
    all_tests.run()

    
