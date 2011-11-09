.. _use:

============
Using CSjark
============

CSjark can be invoked by running the ``csjark.py`` script. The arguments must be specified according to: ::

    csjark.py [-h] [-v] [-d] [-s] [-f [header [header ...]]]
              [-c [config [config ...]]] [-o [output]] [-p] [-n] [-C [cpp]]
			  [-i [header [header ...]]] [-I [directory [directory ...]]]
			  [-D [name=definition [name=definition ...]]]
			  [-U [name [name ...]]] [-A [argument [argument ...]]]
			  [header] [config]
			  
The arguments here specify the following:

``header``
  a c header file to parse.
``config``
  a configuration file to parse.


**Optional arguments:**

    =================================================================================================    ===========================
    ``-h, --help``            		                                                                     Show a help message and exit.
    ``-v, --verbose``                                                                                    Print detailed information.
    ``-d, --debug``              	                                                                     Print debugging information.
    ``-s, --strict``              	                                                                     Only generate dissectors for known structs.
    ``-f [header [header ...]], --file [header [header ...]]``                                           Specifies that CSjark should look for struct definitions in the ``header`` files.
    ``-c [config [config ...]], --config [config [config ...]]``                                         Specifies that the program should use the ``config`` files as configuration.
    ``-o [output], --output [output]``                                                                   Writes the output to the specified file ``output``.
    ``-p, --placeholders``                                                                               Generate placeholder config file for unknown structs
    ``-n, --nocpp``              		                                                                 Disables the C pre-processor.
    ``-C [cpp], --CPP [cpp]``                                                                            Specifies which preprocessor to use.
    ``-i [header [header ...]], --include [header [header ...]]``                                        Process file as Cpp ``#include "file"`` directive
    ``-I [directory [directory ...]], --Includes [directory [directory ...]]``                           Directories to be searched for Cpp includes
    ``-D [name=definition [name=definition ...]], --Define [name=definition [name=definition ...]]``     Predefine name as a Cpp macro
    ``-U [name [name ...]], --Undefine [name [name ...]]``                                               Cancel any previous Cpp definition of name
    ``-A [argument [argument ...]], --Additional [argument [argument ...]]``                             Any additional C preprocessor arguments
    =================================================================================================    ===========================

**Example usage:** ::

    python csjark.py -v headerfile.h configfile.yml

