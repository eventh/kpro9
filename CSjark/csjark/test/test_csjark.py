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
    headers, configs = cli.parse_args([header, '-verbose', '-debug'])
    assert len(headers) == 1

#test for requirement FR07A
@cli.test
def cli_headerfile2(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(include)
    headers, _ = cli.parse_args([header, '-verbose', '-debug', '-i', include])
    assert len(headers) == 2

#test for requirement FR07B
@cli.test
def cli_headerfile_and_configfile(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    config = os.path.join(os.path.dirname(__file__), 'test.yml')
    assert os.path.isfile(config)
    headers, configs = cli.parse_args(
            [header, '-verbose', '-debug', '-i', include, '-config', config])
    assert len(headers) == 2

@cli.test
def cli_flag_verbose(cli):
    """Test the default commandline interface flags"""
    assert cli.verbose == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['-verbose', header])
    assert cli.verbose == True

@cli.test
def cli_flag_debug(cli):
    """Test the default commandline interface flags"""
    assert cli.debug == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['-debug', header])
    assert cli.debug == True

@cli.test
def cli_flag_nocpp(cli):
    """Test the default commandline interface flags"""
    assert cli.use_cpp == True
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    cli.parse_args(['-nocpp', header])
    assert cli.use_cpp == False

@cli.test
def cli_file_dont_existing(cli):
    """Test if a file is missing"""
    with contexts.raises(SystemExit) as error:
        headers, configs = cli.parse_args(['filedontexsist.h', 'test.yml'])
