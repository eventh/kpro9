"""
Module for testing the csjark module. Especially command line interface.
"""

import sys, os
from attest import Tests, assert_hook, contexts

import csjark


cli = Tests()

@cli.context
def create_cli():
    """Create Cli as a context to reset it afterwards."""
    c = csjark.Cli
    defaults = c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file
    yield c
    c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file = defaults

@cli.test
def cli_headerfile1(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    assert os.path.isfile(header)
    headers, configs = cli.parse_args([header, '--verbose', '--debug'])
    assert len(headers) == 1

@cli.test
def cli_headerfile2(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(include)
    headers, _ = cli.parse_args([header, '-v', '-d', '-i', include])
    assert len(headers) == 2

@cli.test
def cli_headerfile_and_configfile(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    config = os.path.join(os.path.dirname(__file__), 'test.yml')
    assert os.path.isfile(config)
    headers, configs = cli.parse_args(
            [header, '--verbose', '-d', '-i', include, '--config', config])
    assert len(headers) == 2

@cli.test
def cli_headerfile_and_configfile_from_folder(cli):
    """Test the support for batch processing"""
    test_folder = os.path.dirname(__file__)
    headers, configs = cli.parse_args([test_folder])
    assert len(headers) > 0 # Requires that test folder has header files

@cli.test
def cli_flag_verbose(cli):
    """Test the default commandline interface flags"""
    assert cli.verbose == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['--verbose', header])
    assert cli.verbose == True

@cli.test
def cli_flag_debug(cli):
    """Test the default commandline interface flags"""
    assert cli.debug == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['--debug', header])
    assert cli.debug == True

@cli.test
def cli_flag_nocpp(cli):
    """Test the default commandline interface flags"""
    assert cli.use_cpp == True
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['--nocpp', header])
    assert cli.use_cpp == False

@cli.test
def cli_file_dont_existing(cli):
    """Test if a file is missing"""
    config = os.path.join(os.path.dirname(__file__), 'test.yml')
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = cli.parse_args(['404.h', config])
    assert str(error) == '2'
    assert out[0].startswith('Unknown file(s): 404.h')

@cli.test
def cli_no_args(cli):
    """Test that providing no arguments prints usage message."""
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = cli.parse_args()
    assert str(error) == '2'
    assert out[0].startswith('usage:')

@cli.test
def cli_no_file(cli):
    """Test that providing no header or config prints usage message."""
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = cli.parse_args(['-v', '-d'])
    assert str(error) == '2'
    assert out[0].startswith('usage:')

@cli.test
def cli_flag_output(cli):
    """Test that one can provide an output argument."""
    # TODO: terje!
    pass

