..
    Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
    Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
    Sigurd Wien and Jaroslav Fibichr.
    
    This file is part of CSjark.
    
    CSjark is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    CSjark is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with CSjark.  If not, see <http://www.gnu.org/licenses/>.


.. _use:

============
Using CSjark
============

CSjark can be invoked by running the ``csjark.py`` script. The arguments must be specified according to: ::

       csjark.py [-h] [-v] [-d] [-s] [-f [header [header ...]]]
                 [-c [config [config ...]]] [-x [path [path ...]]]
                 [-o [output]] [-p] [-n] [-C [cpp]] [-i [header [header ...]]]
                 [-I [directory [directory ...]]]
                 [-D [name=definition [name=definition ...]]]
                 [-U [name [name ...]]] [-A [argument [argument ...]]]
                 [header] [config]
			  
**Required arguments**

``header``
  a C header file to parse or directory which includes header files
``config``
  a configuration file to parse or directory which includes configuration files

Both ``header`` and ``config`` can be:

- file - CSjark processes only the specified file
- directory - CSjark recursively searches the directory and processes all the appropriate files found


**Optional arguments:**

=================================================================================================    ===========================
``-h, --help``            		                                                                     Show a help message and exit.
``-v, --verbose``                                                                                    Print detailed information.
``-d, --debug``              	                                                                     Print debugging information.
``-s, --strict``              	                                                                     Only generate dissectors for known structs.
``-f [header [header ...]], --file [header [header ...]]``                                           Specifies that CSjark should look for struct definitions in the ``header`` files.
``-c [config [config ...]], --config [config [config ...]]``                                         Specifies that the program should use the ``config`` files as configuration.
``-x [path [path ...]], --exclude [path [path ...]]``                                                File or folders to exclude from parsing
``-o [output], --output [output]``                                                                   If ``output`` is a directory, CSjark saves the output dissectors into this directory, 
                                                                                                     otherwise CSjark saves the output dissectors into one specified file named ``output``.
``-p, --placeholders``                                                                               Automatically generates configuration files with placeholders for structs without configuration. More in section :ref:`configfile`. 
``-n, --nocpp``              		                                                                 Disables the C pre-processor.
``-C [cpp], --CPP [cpp]``                                                                            Specifies which preprocessor to use.
``-i [header [header ...]], --include [header [header ...]]``                                        Process file as Cpp ``#include "file"`` directive
``-I [directory [directory ...]], --Includes [directory [directory ...]]``                           Additional directories to be searched for Cpp includes.
                                                                                                     The directories included are added as an argument to the preprocessor.
                                                                                                     The preprocessor can search there for those files, which are given in an ``#include`` directive of the C header input.
``-D [name=definition [name=definition ...]], --Define [name=definition [name=definition ...]]``     Predefine name as a Cpp macro
``-U [name [name ...]], --Undefine [name [name ...]]``                                               Cancel any previous Cpp definition of name
``-A [argument [argument ...]], --Additional [argument [argument ...]]``                             Any additional C preprocessor arguments
=================================================================================================    ===========================

**Example usage:** ::

    python csjark.py -v -o dissectors headerfile.h configfile.yml

**Batch mode**

One of the most important features of CSjark is processing multiple C header files in one run. That can be easily achieved by specifying a directory instead of a single file as command line argument (see above): ::

    python csjark.py headers configs
    
In batch mode, CSjark only generates dissectors for structs that have a configuration file with an ID (see section :ref:`ids` for information how to specify dissector message ID), and for structs that depend on other structs. This speeds up the generation of dissectors, since it only generates dissectors that Wireshark can use.



