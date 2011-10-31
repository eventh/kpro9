=================
Installing CSjark
=================

Dependencies
------------

CSjark is written in Python 3.2, and will therefore need Python 3.2 or later to run. This can be obtained from http://www.python.org/. Instructions for installation can also be found there.

There are three 3. party dependencies to get CSjark working:

1: pycpaser.
    Pycparser is a C parser that is implemented in Python. It can be obtained from http://code.google.com/p/pycparser/. Pycparser depends on PLY with can be obtained from http://www.dabeaz.com/ply/. Both websitedsites contains instructions for installation and more information about their functionality.

    Warning: The _Bool type is not supported in the 2.04 release of pycparser, but it is in the current developer code. To get it, visit http://code.google.com/p/pycparser/source/checkout .
    Optimalization: To get the pycparser library to work faster, navigate to the folder that pycparser

2: C-preprocessor.
    CSjark requires a C-preprocessor. On Windows one is bundled with CSjark, but for osx, linux or solaris, it will need to be installed separately. Under OSX, this can for example be done simply by installing Xcode.

3:  pyYAML
    pyYAML is a parser for YAML. YAML is the language used to specify configurations to CSjark. To get PYparser, please visit http://pyyaml.org/wiki/PyYAML. The webside includes both a way to download the software and a short desciption on how to install it.

To get the proper lua integration to so that the lua dissectors that CShark generates can work, the latest development version of Wireshark (version 1.7 dev) is required. It can be obtained from this website: http://www.wireshark.org/download/automated/ . Browse to the proper folder for the platform that you are on, and download the latest.


CSjark
------

CSjark can be obtained at https://github.com/eventh/kpro9/.
CSjark itself requires no installation. After the steps described in the dependencies section is completed. It can be ran by opening a terminal, navigating to the directory containing ``cshark.py`` and invoking as described in section :ref:`use`.

