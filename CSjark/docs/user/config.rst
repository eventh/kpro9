Configuration
=============

Configuration format
--------------------

The configuration files are written in YAML which is a data serialization format designed to be easy to read and write. The format of the files are described below. The configuration should be put in a ``filename.yml`` file and specified when running CSjark with the ``-config`` commandline argument.


Configuration definitions
-------------------------

Value ranges
~~~~~~~~~~~~

Some variables may have a domain that is smaller than its given type. You could for example use an integer to describe percentage, which is a number between 0 and 100. It is possible to specify this to CSjark, so that the resulting dissector will tell wireshark if the values are in range or not. Value ranges are defined by the following syntax: ::

    RangeRules:
      - struct: "Name of the struct"
        member: "Name of datameber"
        min: "Lowest allowed value"
        max: "Highest allowed value"

or, one could specify a type, and apply the value range to all the members of that type within the struct: ::

    RangeRules:
      - struct: "Name of the struct"
        type: "Name of the type"
        min: "Lowest allowed value"
        max: "Highest allowed value"

Example: ::

    RangeRules:
      - struct: example_struct
        member: percent
        min: 0
        max: 100
    
      - struct: example_struct
        type: int
        min: 0
        max: 100
    
Bitstrings
~~~~~~~~~~

It is possible to configure bitstrings in the utility. This makes it possible to view common data types like integer, short, float, etc. used as a bitstring in the wireshark dissector.

There is two ways to configure bitstrings, the first one is to specify a struct member and define the bit representation. The second option is to specify bits for all struct members of a given type.

These rules specifies the config:

- The bits are specified as 0...n, where 0 is the most significant bit
- A bit group can be one or more bits.
- Bit groups have a name
- It is possible to name all possible values in a bit group.

Member Config
#############

Below, there is an example of a configuration for the flags member of the struct example. This example has four bits specified, the first bit group is named "In use" and represent bit 0. The second group represent bit 1 and is named "Endian", and the values are named: 0 = "Big", 1 = "Little". The last group is "Platform" and represent bit 2-3 and have 4 named values.

::

    Structs:
      - name: example
        id: 1000
        description: An example
        bitstrings:
          - member: flags
            0: In use
            1: [Endian, Big, Little]
            2-3: [Platform, Win, Linux, Mac, Solaris]

Type Config
###########

This example specifies a bitstring for all data types of short. ::

    Structs:
      - name: example
        id: 1000
        description: An example
        bitstrings:
          - type: short
            0: Red
            1: Green
            2: Blue


Dissector ID
~~~~~~~~~~~~~~~~~~

All struct-packets that Wireshark captures, has a header, one of the ﬁelds in 
the header is the message id. This id is used to load the the correct dissector 
when a packet is captured. Each dissector should have a unique id, to avoid 
possible conﬂicts. This functionallity is implemented and the message id
must be speciﬁed in the conﬁguration ﬁle, Listing 1.8 is an example of how 
this is done. 

Value explanations
~~~~~~~~~~~~~~~~~~

Some variables may actually represent other values than its type. For example, for an enum it could be preferable to get the textual name of the value displayed, instead of the integer value that represent it. For enums, this will usually happen automaticlly, but if there are other types that does something similar, it needs to be provided manually. This can be done by:

*Insert when implemented*

External Lua dissectors
~~~~~~~~~~~~~~~~~~~~~~~

Sometimes CSjark will not be able to deliver the desired result from its own analysis, and the configuration options above may be too constraining. In this case, it is possible to write the lua dissector by hand, either for a given member or for an entire struct. This can be done with the following syntax:

*Insert when implemented*