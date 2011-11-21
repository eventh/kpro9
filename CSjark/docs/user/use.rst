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
                 [-o [output]] [-p] [-n] [-C [path]] [-i [header [header ...]]]
                 [-I [directory [directory ...]]]
                 [-D [name=definition [name=definition ...]]]
                 [-U [name [name ...]]] [-A [argument [argument ...]]]
                 [header] [config]

**Example usage:** ::

    python csjark.py -v -o dissectors headerfile.h configfile.yml

**Batch mode**

One of the most important features of CSjark is processing multiple C header files in one run. That can be easily achieved by specifying a directory instead of a single file as command line argument (see above): ::

    python csjark.py headers configs
    
In batch mode, CSjark only generates dissectors for structs that have a configuration file with an ID (see section :ref:`ids` for information how to specify dissector message ID), and for structs that depend on other structs. This speeds up the generation of dissectors, since it only generates dissectors that Wireshark can use.

**Required arguments**

``header``
  a C header file to parse or directory which includes header files
``config``
  a configuration file to parse or directory which includes configuration files

Both ``header`` and ``config`` can be:

- file - CSjark processes only the specified file
- directory - CSjark recursively searches the directory and processes all the appropriate files found


**Optional argument list**

===========================================  ===========================
:option:`-h`, :option:`--help <-h>`          Show a help message and exit.
:option:`-v`, :option:`--verbose <-v>`       Print detailed information.
:option:`-d`, :option:`--debug <-d>`         Print debugging information.
:option:`-s`, :option:`--strict <-s>`        Only generate dissectors for known structs.
:option:`-f`, :option:`--file <-f>`          Additional locations of header files.
:option:`-c`, :option:`--config <-c>`        Additional locations of configuration files.
:option:`-x`, :option:`--exclude <-x>`       File or folders to exclude from parsing.
:option:`-o`, :option:`--output <-o>`        Location for storing generated dissectors.
:option:`-p`, :option:`--placeholders <-p>`  Automatically generates config files with placeholders.
:option:`-n`, :option:`--nocpp <-n>`         Disables the C pre-processor.
:option:`-C`, :option:`--Cpppath <-C>`       Specifies the path to C preprocessor.
:option:`-i`, :option:`--include <-i>`       Process file as Cpp `#include "file"` directive
:option:`-I`, :option:`--Includes <-I>`      Additional directories to be searched for Cpp includes.
:option:`-D`, :option:`--Define <-D>`        Predefine name as a Cpp macro
:option:`-U`, :option:`--Undefine <-U>`      Cancel any previous Cpp definition of name
:option:`-A`, :option:`--Additional <-A>`    Any additional C preprocessor arguments
===========================================  ===========================

**Optional argument details**

.. cmdoption:: -h, --help

    Show a help message and exit.
    
.. cmdoption:: -v, --verbose                                                                                     

    Print detailed information.

.. cmdoption:: -d, --debug              	                                                                        
    
    Print debugging information.

.. cmdoption:: -s, --strict              	                                                                     

    Only generate dissectors for known structs. As known structs we consider only structs for which exists valid configuration file with ID defined. Also, CSjark generates dissectors for structs that depend on known structs.  

.. cmdoption:: -f [path [path ...]], --file [path [path ...]]
                                           
    Specifies that CSjark looks for struct definitions in the `path`. There can be more than one path specified, separated by whitespace. As `path` there can be file and directory. In case of a directory, CSjark searches for header files recursively to maximum possible depth. 
    
    All header files found are added to the files specified by the required ``header`` argument. 

    
    Example::
    
        csjark.py -f hdr/file1.h dir1 file2.h


.. cmdoption:: -c [path [path ...]], --config [path [path ...]]                                         
    
    Specifies that CSjark looks for configuration definition files in the `path`. There can be more than one path specified, separated by whitespace. As `path` there can be file and directory. In case of a directory, CSjark searches for configuration files recursively to maximum possible depth.
    
    All configuration files found are added to the files specified by the required ``config`` argument.
    
    Example::
    
        csjark.py -c etc/conf1.yml dir1 conf2.yml


.. cmdoption:: -x [path [path ...]], --exclude [path [path ...]]
                                                
    File or folders to exclude from parsing. 
    
    When using the option, CSjark will not search for header files in the `path`. There can be more than one path specified, separated by whitespace. As `path` there can be file and directory. In case of a directory, CSjark will skip header files also in its subdirectories.

.. cmdoption:: -o [path], --output [path]       

    Sets location for storing generated dissectors.                                                            

    If `path` is a directory, CSjark saves the output dissectors into this directory, otherwise CSjark saves the output dissectors into one specified file named `path`. If file with this name already exists, it is rewritten without warning.
    
    *Default:* CSjark root directory (when the `csjark.py` file is located)

.. cmdoption:: -p, --placeholders                                                                              

    Automatically generates configuration files with placeholders for structs without configuration. 
    
    More in section :ref:`configfile`. 

.. cmdoption:: -n, --nocpp              	                                                                 

    Disables the C pre-processor. 

.. cmdoption:: -C [path], --Cpppath [path]                                                                      

    Specifies the path to the external C preprocessor. 
    
    Default: 
     - Windows, the path is `../utils/cpp.exe` (uses cpp bundled with CSjark).    

.. cmdoption:: -i [header [header ...]], --include [header [header ...]]                                        

    Process `header` as if `#include "header"` appeared as the first line of the input header files

.. cmdoption:: -I [directory [directory ...]], --Includes [directory [directory ...]]                           
    
    Additional directories to be searched for Cpp includes. 
    
    Add the directory `directory` to the list of directories to be searched for header files. These directories are added as an argument to the preprocessor. The preprocessor can search there for those files, which are given in an `#include` directive of the C header input.

.. cmdoption:: -D [name=definition [name=definition ...]], --Define [name=definition [name=definition ...]]     
    
    Predefine `name` as a Cpp macro, with definition `definition`.   

.. cmdoption:: -U [name [name ...]], --Undefine [name [name ...]]                                               
    
    Cancel any previous Cpp definition of name, either built in or provided with a :option:`-D` option.

.. cmdoption:: -A [argument [argument ...]], --Additional [argument [argument ...]]                             

    Any additional C preprocessor arguments.
    
    Adds any other arguments (additional to `-D`, `-U` and `-I`) to the preprocessor.

