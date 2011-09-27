"""
Module for testing the csjark module. Especially command line interface.
"""

import sys, os
from attest import Tests, assert_hook

try:
    import csjark
except ImportError:
    # If csjark is not installed, look in parent folder
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))
    import csjark

cli = Tests()

@cli.test
def cli_test_header():
    assert True

@cli.test
def cli_test_flag_default():
    """Test the default commandline interface flags"""
    assert csjark.Cli.verbose == False
    assert csjark.Cli.debug == False
    assert csjark.Cli.use_cpp == True


if __name__ == '__main__':
    all_tests = Tests([cli])
    all_tests.run()

    
