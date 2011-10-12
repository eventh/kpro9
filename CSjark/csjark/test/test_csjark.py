"""
Module for testing the csjark module. Especially command line interface.
"""

import sys, os
from attest import Tests, assert_hook

import csjark


cli = Tests()

@cli.test
def cli_headerfile1():
    """Test the default commandline interface flags"""
    headers, configs = csjark.Cli.parse_args(['cpp.h', '-verbose', '-debug'])
    assert len(headers) == 1

#test for requirement FR07A
@cli.test
def cli_headerfile2():
    """Test the default commandline interface flags"""
    headers, configs = csjark.Cli.parse_args(['cpp.h', '-verbose', '-debug',
                                              '-i', 'include.h'])
    assert len(headers) == 2

#test for requirement FR07B
@cli.test
def cli_headerfile_and_configfile():
    """Test the default commandline interface flags"""
    headers, configs = csjark.Cli.parse_args(['cpp.h', '-verbose', '-debug',
                                              '-i', 'include.h', '-config', 'test.yml'])
    assert len(headers) == 2

@cli.test
def cli_flag_verbose():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-verbose', 'cpp.h'])
    assert csjark.Cli.verbose == True

@cli.test
def cli_flag_debug():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-debug', 'cpp.h'])
    assert csjark.Cli.debug == True

@cli.test
def cli_flag_nocpp():
    """Test the default commandline interface flags"""
    csjark.Cli.parse_args(['-nocpp', 'cpp.h'])
    assert csjark.Cli.use_cpp == False

@cli.test
def cli_file_dont_existing():
    """Test if a file is missing"""
    headers, configs = csjark.Cli.parse_args(['filedontexsist.h', 'test.yml'])
    assert ''
