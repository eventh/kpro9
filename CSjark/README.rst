==========================================
CSjark: Tool for generating Lua dissectors
==========================================

Summary
-------
CSjark is a tool for generating Lua dissectors from C struct definitions
to use with Wireshark. Wireshark is a leading tool for capturing and
analysing network traffic. The goal with the dissectors is to make
Wireshark able to nicely display the values of a struct sent over the
network, along with member names and type. This can be a powerful tool
for debugging C programs that communicates with strucs over the network.

Requirements
------------
* Python v3.2.2 or later
* `PLY (Python Lex-Yacc) v3.4 <http://www.dabeaz.com/ply/>`_
* `Pycparser v2.07 <http://code.google.com/p/pycparser/>`_
* `pyYAML v3.10 <http://pyyaml.org/wiki/PyYAML>`_
* `Wireshark v1.7-dev <http://www.wireshark.org/>`_ (to use)
* `Attest v0.6 <http://packages.python.org/Attest/>`_ (for tests)

Run unittests
-------------
To run the unittests checkout sources and run:
"python -m attest" in the CSjark/csjark/ folder.

Documentation
-------------
* User documentation: http://csjark.readthedocs.org/
* Development documentation: http://csjark.readthedocs.org/
* GitHub project page: https://github.com/eventh/kpro9

License
-------
CSjark is licensed under the GPLv3. See separate LICENSE.txt.
Copyright (C) 2011 Even Wiik Thomassen, Erik Bergersen,
Sondre Johan Mannsverk, Terje Snarby, Lars Solvoll Tønder,
Sigurd Wien and Jaroslav Fibichr.

