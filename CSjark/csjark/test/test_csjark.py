# -*- coding: utf-8 -*-
# Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
# Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
# Sigurd Wien and Jaroslav Fibichr.
#
# This file is part of CSjark.
#
# CSjark is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# CSjark is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CSjark.  If not, see <http://www.gnu.org/licenses/>.
"""
Module for testing the csjark module. Especially command line interface.
"""

import sys, os
from attest import Tests, assert_hook, contexts

import csjark
import config
import cparser
import dissector


# Tests for the command line interface.
cli = Tests()

@cli.context
def create_cli():
    """Create Cli as a context to reset it afterwards."""
    c = config.Options
    defaults = c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file
    yield c
    c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file = defaults

@cli.test
def cli_headerfile1(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    assert os.path.isfile(header)
    headers, configs = csjark.parse_args([header, '--verbose', '--debug'])
    assert len(headers) == 1

@cli.test
def cli_headerfile2(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(include)
    headers, _ = csjark.parse_args([header, '-v', '-d', '-f', include])
    assert len(headers) == 2

@cli.test
def cli_headerfile_and_configfile(cli):
    """Test the default commandline interface flags"""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    config = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
    assert os.path.isfile(config)
    headers, configs = csjark.parse_args(
            [header, '--verbose', '-d', '-f', include, '--config', config])
    assert len(headers) == 2

@cli.test
def cli_headerfile_and_configfile_from_folder(cli):
    """Test the support for batch processing"""
    test_folder = os.path.dirname(__file__)
    headers, configs = csjark.parse_args([test_folder])
    assert len(headers) > 0 # Requires that test folder has header files

@cli.test
def cli_flag_verbose(cli):
    """Test the default commandline interface flags"""
    assert cli.verbose == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    csjark.parse_args(['--verbose', header])
    assert cli.verbose == True

@cli.test
def cli_flag_debug(cli):
    """Test the default commandline interface flags"""
    assert cli.debug == False
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    csjark.parse_args(['--debug', header])
    assert cli.debug == True

@cli.test
def cli_flag_nocpp(cli):
    """Test the default commandline interface flags"""
    assert cli.use_cpp == True
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    csjark.parse_args(['--nocpp', header])
    assert cli.use_cpp == False

@cli.test
def cli_file_dont_existing(cli):
    """Test if a file is missing"""
    config = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = csjark.parse_args(['404.h', config])
    assert str(error) == '2'
    assert out[0].startswith('Unknown file(s): 404.h')

@cli.test
def cli_no_args(cli):
    """Test that providing no arguments prints usage message."""
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = csjark.parse_args()
    assert str(error) == '2'
    assert out[0].startswith('usage:')

@cli.test
def cli_no_file(cli):
    """Test that providing no header or config prints usage message."""
    with contexts.capture_output() as (out, err):
        with contexts.raises(SystemExit) as error:
            headers, configs = csjark.parse_args(['-v', '-d'])
    assert str(error) == '2'
    assert out[0].startswith('usage:')

@cli.test
def cli_only_config(cli):
    """Test that one can provide only a yaml file."""
    config = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
    assert os.path.isfile(config)
    headers, configs = csjark.parse_args([config])
    assert len(headers) == 0
    assert len(configs) == 1

@cli.test
def cli_output_dir(cli):
    """Test that one can provide an output folder argument."""
    assert cli.output_file is None
    assert cli.output_dir is None
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    config = os.path.join(os.path.dirname(__file__), 'sprint3.yml')
    folder = os.path.dirname(__file__)
    headers, configs = csjark.parse_args([header, config, '-o', folder])
    assert cli.output_file is None
    assert cli.output_dir == folder

@cli.test
def cli_output_file(cli):
    """Test that one can provide an output file argument."""
    assert cli.output_file is None
    assert cli.output_dir is None
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    config = os.path.join(os.path.dirname(__file__), 'sprint3.yml')
    out_file = os.path.join(os.path.dirname(__file__), 'out_file.lua')
    headers, configs = csjark.parse_args([header, config, '-o', out_file])
    assert cli.output_file == out_file
    assert cli.output_dir is None

@cli.test
def parse_headers(cli):
    """Test the parse header function in csjark module."""
    headers = [os.path.join(os.path.dirname(__file__), i)
                for i in ('sprint2.h', 'sprint3.h', 'cpp.h')]
    tmp, configs = csjark.parse_args([headers[0], '-v', '-d'])
    failed = csjark.parse_headers(headers)
    assert failed == 0
    # Cleanup
    cparser.StructVisitor.all_protocols = {}
    dissector.Protocol.protocols = {}

