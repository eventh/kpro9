==================
Testing
==================

There are several types of tests done for verification of CSjark functionality:


White box testing
-----------------
This type of white box testing basically means verification of functionality of specific section of the code, usually at the function level. As a tool for creating white box unit tests, the team decided to use the Attest_ testing framework for python code.

Black box testing
-----------------
In general black box testing does not require the tester to have any intimate knowledge about the system or any of the programming logic that went into making it. Black box test cases are built around the specifications and requirements of a system, for example its functional, and in some cases, non-functional requirements.

For CSjark, black box testing means feeding the utility with input C header file, corresponding configuration file and generating the output (Lua dissector). Then, the generated output is compared to expected output.

Another way how to do the black box testing to use the generated dissectors in Wireshark. For this purpose, we also need a ``pcap`` file containing the IPC packets that corresponds to the input C header files. You can read more about whole process in the User Manual section :ref:`intro`. A short guide how to create ``pcap`` file for the C struct can be found in the `project wiki`_.

With the generated Lua dissectors, it should possible to display the contents of the C struct within the IPC packets. Also, according to the utility requirements, it should be possible to filter and search by any variable name or its value. This way of testing is based on manual checking of the individual variable values. The process involves several manual steps and therefore cannot be automated.

.. _`project wiki`: https://github.com/eventh/kpro9/wiki/text2pcap 


Regression testing
----------------------------------

The test must be written in a way that it should be possible to run them repeatedly after the first run. That can ensure that all the implemented functionality is still working well after changes in the code.


Creating tests
--------------

To create tests using Attest, you start by importing ``Tests``, ``assert_hook`` and optionally ``contexts`` from ``attest`` library. You then create a variable and initialize it to an instance of Tests, which is the variable that will contain list functions that each constitutes one test that is to be run. To feed your test instance with functions for testing you then have to mark these functions with a decorator and feed it the ``.tests`` function of the Tests instance. After creating a unit test in this fashion you can run all of your unit tests through Attest from the command line by typing::

    python -m attest
    
This runs all of your unit tests through Attest and returns a message telling the user how many assertions failed, as well as what input made them fail. For more information read the user documentation of Attest_.

.. _Attest: http://packages.python.org/Attest/


Testing code
------------

All the test code, the testing configuration files and the testing input files are located in folder

    `CSjark/csjark/test <https://github.com/eventh/kpro9/tree/master/CSjark/csjark/test>`_

It contains modules for unit/module testing of each of the CSjark modules as well as modules for bundled white/black box testing.   
