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


Welcome to CSjark's documentation!
==================================

CSjark is a tool for generating Lua dissectors from C struct definitions to use with Wireshark. Wireshark is a leading tool for capturing and analysing network traffic. The goal with the dissectors is to make Wireshark able to nicely display the values of a struct sent over the network, along with member names and type. This can be a powerful tool for debugging C programs that communicates with strucs over the network.

For more information about Wireshark please visit `Wireshark website <http://www.wireshark.org>`_.


User Documentation
------------------

.. toctree::
   :maxdepth: 2

   user/install
   user/use
   user/use_ws
   user/config

..
    Developer Documentation
    -----------------------

    .. toctree::
       :maxdepth: 2

    ..
        deve/devel

Other Information
-----------------

.. toctree::
   :maxdepth: 2

   other/license
   other/about

------------

..
    **Feature list** (TBD)

    - C header files
    - Batch mode
    - Searching and filtering in Wireshark
    - ...

**Currently supported platforms**

- Windows 32-bit
- Windows 64-bit
- Solaris 32-bit
- Solaris 64-bit
- Solaris SPARC 64-bit
- MacOS
- Linux 32 bit

(additional platforms can be added by configuration)


..
    Indices and tables
    ------------------

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`

