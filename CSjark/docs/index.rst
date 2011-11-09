.. CSjark documentation master file, created by
   sphinx-quickstart on Thu Sep 22 18:47:43 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CSjark's documentation!
==================================

CSjark is a tool for generating Lua dissectors from C struct definitions to use with Wireshark. Wireshark is a leading tool for capturing and analysing network traffic. The goal with the dissectors is to make Wireshark able to nicely display the values of a struct sent over the network, along with member names and type. This can be a powerful tool for debugging C programs that communicates with strucs over the network.

For more information about Wireshark please visit http://www.wireshark.org.



**Features** (TBD)

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


User Documentation
------------------

.. toctree::
   :maxdepth: 2
   
   user/install
   user/use
   user/use_ws
   user/config

Developer Documentation
-----------------------

.. toctree::
   :maxdepth: 2

..   
   devel/devel

Other Information
-----------------

.. toctree::
   :maxdepth: 2
   
   other/whatsnew
   other/limits
   other/license
   other/copyright
   other/about


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

