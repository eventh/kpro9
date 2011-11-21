===================
 Design Overview
===================

This part describes the design of the CSjark to help all the future developers to understand what is under the hood.

Textual description
-------------------

CSjark starts with the `csjark` module. It takes as input command line arguments, including file and folder names for C header files and configuration files.
It replaces folder names with the file names of the files inside the folders, and checks that all the files exists, then it gives the names of the configuration files to the `config` module.

The `config` module parses configuration files and stores them in suitable config data structures in memory. It takes as input file names, and it opens those files to read their content.

`Csjark` module then gives file names of C header files to the `cpp` module. The `cpp` module gives the file names and some other arguments to an external program, the C preprocessor (`cpp.exe` on Windows). This external program opens the header files, and when it encounters `#include` directives it searches for the right file and opens it as well. The output of this external program is just a long string of C code, which `cpp` module returns to the `csjark` module.

The `csjark` module then gives the C code string to `cparser` module, which forwards the string to pycparser. Pycparser parse the C code to generate an abstract syntax tree, which it returns to `cparser` which returns it to `csjark`.

Csjark module then tells `cparser` to find all struct definitions in the abstract syntax tree, which it does by traversing the tree. Each time it finds a struct, it asks `dissector` module to create a protocol for it. Afterwards `cparser` holds a list of all the created protocols.

Csjark then gets the list of protocols from `cparser`, and for each one asks `dissector` module to generate lua code for Wireshark dissectors. It writes these dissectors to files, and finishes with a status message informing the user how it all went.

The new `field` module is simply to move class `Fields` and its sub-classes into their own module to make `dissector` module smaller and less complex.

**Summary**
 
`csjark` module writes Lua files, `config` module opens and reads YAML files, `cpp` module starts an external program which reads C header files. The structure as well as the associations among the classes are shown on following module_ and class_ diagrams.

.. _module:

Module diagram
--------------

.. figure:: /img/module_diagram.png
    :alt: CSjark module diagram
    :align: center
    :width: 60%

    `CSjark: module diagram`

.. _class:

Class diagram
-------------

.. figure:: /img/class_diagram.png
    :alt: CSjark class diagram
    :align: center
    :width: 90%

    `CSjark: class diagram`