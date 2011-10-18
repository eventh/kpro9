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

Enums
~~~~~

Values of integer variables can be assigned to string values similarly to enumerated values in most programming languages. Thus, instead of integer value, a corresponding value defined in configuration file as a enumeration can be displayed. 

The enumeration definition can be of two types. The first one, mapping specified integer by its struct member name, so it gains string value dependent on the actual integer value. And the second, where assigned string values correspond to every struct member of the type defined in the configuration.

The enum definition, as an attribute of the ``Structs`` item of the configuration file, always starts by ``enums`` keyword. It is followed by list of members/types for which we want to define enumerated integer values for. Each list item consists 2 mandatory and 1 optional value
::

    - member | type: member name | type name
      values: [value1, value2, ...] | { key1: value1, key2: value2, ...}
      strict: True | False

where 

- ``member name``/``type name`` contains string value of integer variable name for which we want to define enumerated values
- ``[value1, value2, ...]`` is comma-separated list of enumerated values (implicitly numbered, starting from 0) 
- ``{ key1: value1, key2: value2, ...}`` is comma-separated list of key-value pairs, where ``key`` is integer value and ``value`` is it's assigned string value
- ``strict`` is boolean value, which disables warning, if integer does not contain a value specified in the enum list (default ``True``)
    


Member Config
#############

Example of Struct definition with member named ``weekday`` and values defined as a list of key-value pairs.

::

    Structs:
      - name: enum_example1
        id: 10
        description: Enum config example 1
        enums:
          - member: weekday
            values: {1: MONDAY, 2: TUESDAY, 3: WEDNESDAY, 4: THURSDAY, 5: FRIDAY, 6: SATURDAY, 7: SUNDAY}

Type config
###########

In this example we can see definition of enumerated values for ``int`` type. Values are given by simple list, therefore numbering is implicit (starting from 0, i.e. ``Blue`` = 2). Warning in case of invalid integer value *will* be displayed.

::

    Structs:
      - name: enum_example2
        id: 10
        description: Enum config example 2
        enums:       
          - type: int
            values: [Black, Red, Blue, Green, Yellow, White]
            strict: True # Disable warning if not a valid value


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

In every struct-packet that Wireshark captures, there is a header. One of the fields in the header, the id field, specifies which dissector that should be loaded to dissect the actual struct. This field can be specified in the configuration file. If no configfile is given, the packet will be assigned a default dissector.  

This is an example of the specification ::

    Structs: 
	−name: structname 
	id: 10 

Value explanations
~~~~~~~~~~~~~~~~~~

Some variables may actually represent other values than its type. For example, for an enum it could be preferable to get the textual name of the value displayed, instead of the integer value that represent it. For enums, this will usually happen automaticlly, but if there are other types that does something similar, it needs to be provided manually. This can be done by:

*Insert when implemented*

External Lua dissectors
~~~~~~~~~~~~~~~~~~~~~~~

Sometimes CSjark will not be able to deliver the desired result from its own analysis, and the configuration options above may be too constraining. In this case, it is possible to write the lua dissector by hand, either for a given member or for an entire struct. This can be done with the following syntax:

*Insert when implemented*

Configuration of various trailers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

CSjark only creates dissectors from c-struct, to be able to use built-in dissectors in wireshark, it is necessary to configure it. Wireshark has more than 1000 built-in dissectors. Several trailer can be configured for a packet.

The following parameters is allowed in trailers:
- name: The protocol name for the built-in dissector
- count: The number of trailers
- member: Struct member, that contain the amount of trailers
- size: Size of the buffer to feed to the protocol

There are two ways to configure the trailers, specifiy the total number of trailers or give a variable in the struct, which contains the amount of trailers. The two ways to configure trailers are listed below.

	trailers:
	  - name: "protocol name"
	  - member: "variable in struct, which contain amount of trailers"
	  - size: "size of the buffer"

	trailers:
	  - name: "protocol name"
	  - count: "Number of trailers"
	  - size: "size of the buffer"

Example:
The example below shows an example with BER\footnote{Basic Encoding Rules}, which av 4 trailers with a size of 6 bytes.

	trailers:
	  - name: ber
	  - count: 4
	  - size: 6
