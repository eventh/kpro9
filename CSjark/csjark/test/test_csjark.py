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
def cli_test_flag_verbose():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-verbose', 'cpp.h'])
    assert csjark.Cli.verbose == True

@cli.test
def cli_test_flag_debug():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-debug', 'cpp.h'])
    assert csjark.Cli.debug == True

@cli.test
def cli_test_flag_nocpp():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-nocpp', 'cpp.h'])
    assert csjark.Cli.use_cpp == False


if __name__ == '__main__':
    all_tests = Tests([cli])
    all_tests.run()

