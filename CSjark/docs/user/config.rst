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

..
    header  = - _ ~ ^ #

===============
 Configuration
===============

Because there exists distinct requirements for flexibility of generating dissectors, CSjark supports configuration for various parts of the program. First, general parameters for utility running can be set up. This can be for example settings of variable sizes for different platforms or other parameters that could determine generating dissectors regardless actual C header file. Second, each individual C struct can be treated in different way. For example, value of specific struct member can be checked for being within specified limits. 

.. contents:: Contents
   :depth: 4


.. _configfile:

Configuration file format and structure
---------------------------------------

**Format**

The configuration files are written in YAML_ which is a data serialization format designed to be easy to read and write. The configuration must be put in a ``filename.yml`` file and specified when running CSjark as a command line argument (more about CLI in section :ref:`use`).

Basic YAML syntax is shown on following example: ::

    # comments can start anywhere with number sign (#) and continues until the end of the line

    key1: value1                   # associative array of two key-value pairs 
    key2: value2                   # pairs are separated by colon (:) and space ( ) on a separate line
    
    {key3: value3, key4: value4}   # inline format of specifying associative arrays 
                                   # pairs are separated by comma (,) and enclosed into curly braces ({})
                                   
    - item1                        # list of two items
    - item2                        # each item starts with hyphen (-) and space ( ) on a separate line
        
    [item3, item4]                 # inline format of the list
                                   # items are separated by comma (,) and enclosed into square brackets ([])

Data structure hierarchy in YAML is maintained by outline indentation (whitespace is used, tab not allowed). All the basic elements can be combined to create a hierarchy: ::

    Options:
        use_cpp:                True
        generate_placeholders:  True      
    
    Structs:
      - name:   struct1
        id:     [10, 12, 14]
      - name:   struct2
        id:     [11, 13, 15]


Strings are ordinarily unquoted, but may be enclosed in double-quotes ("), or single-quotes ('). The specific number of spaces in the indentation is unimportant as long as parallel elements have the same left justification and the hierarchically nested elements are indented further. This sample defines an associative array with 2 top level keys: one of the keys, "Structs", contains a 2 element array (or "list"), each element of which is itself an associative array with differing keys.

Detailed specification can be found at `YAML website <http://www.yaml.org/spec/1.2/spec.html>`_.

**Structure**

CSjark configuration files consist of 2 main parts. The first part is used for specifing all the configuration corresponding CSjark processing in general. More about CSjark options in `Options Configuration`_. The second part contains configuration for individual C struct definitions. That is described in section `Struct Configuration`_.

The configuration file may have following strucuture: ::

    Options:
      # there will be all your CSjark processing configuration
      use_cpp: True
      ...
    
    Structs:
      # there will be a sequence of Struct definition configurations
      - name: struct1
        id: [10, 12, 14]
        # another struct1 config
      - name: struct2
        id: [11, 13, 15]
        # another struct2 config

**Automatic generation of configuration files**

Autogeneration of configuration file is a simple feature, that could save the user of the utility some time, since  the essential part of the configuration file is generated automatically.  The utility will only create a new file, containg the name of the struct and line to specifiy the ID for the dissector.  To generate the configuration file, the utility must be run with ``-p`` or ``--placeholders`` as an option (see :ref:`use` for more about CSjark CLI).

    
.. note::
    One part of the configuration is held directly in the code. It represents the platform specific setup (file ``platform.py``) - see `Platform specific configuration`_.


Struct Configuration
--------------------

Each individual C struct processed by CSjark can be treated in different way. All the configuration settings must be done in the ``Structs`` section of the configuration file. Every Struct definition is one item of the sequence and may contain these attributes:

==============  =============
Attribute name  Description
==============  =============
name            C struct name (required field) 
id              Dissector message id - more in `Dissector message ID`_
description     Struct name displayed in Wireshark
size            Size of the struct in memory - more in `Unknown structs handling`_
cnf             Conformance file name - more in `External Lua dissectors`_
ranges          Value ranges limitations - more in `Value ranges`_
enums           Enumeration definitions - more in `Enums`_
bitstrings      Bitstrings definitions - more in `Bitstrings`_
trailers        Trailers definitions - more in `Trailers`_
customs         Definitions for custom struct member handling - more in `Custom handling of data types`_
==============  =============


Value ranges
~~~~~~~~~~~~

Some variables may have a domain that is smaller than its given type. You could for example use an integer to describe percentage, which is a number between 0 and 100. It is possible to specify this to CSjark, so that the resulting dissector will tell Wireshark if the values are in the specified range or not. Value ranges are defined by the following syntax: ::

    Structs:
      - name: "Name of the struct"
        id: 989
        ranges:
            - member | type: "Name of struct member / type"
              min: "Lowest allowed value"
              max: "Highest allowed value"
              

When the definition specified as a type, the value range is applid to all the members of that type within the struct.

Example: ::

    Structs:
      - name: example_struct
        id: 90
        ranges:
            - member: percent
              min: 0
              max: 100
            - type: int
              min: -10
              max: 10

Value explanations
~~~~~~~~~~~~~~~~~~

Some variables may actually represent other values than its type. For example, for an enum it could be preferable to get the textual name of the value displayed, instead of the integer value that represent it. Such example can be an enum type or a bitstring.



Enums
^^^^^

Values of integer variables can be assigned to string values similarly to enumerated values in most programming languages. Thus, instead of integer value, a corresponding value defined in configuration file as a enumeration can be displayed. 

The enumeration definition can be of two types. The first one, mapping specified integer by its struct member name, so it gains string value dependent on the actual integer value. And the second, where assigned string values correspond to every struct member of the type defined in the configuration.

The enum definition, as an attribute of the ``Structs`` item of the configuration file, always starts by ``enums`` keyword. It is followed by list of members/types for which we want to define enumerated integer values for. Each list item consists of 2 mandatory and 1 optional values
::

    - member | type: member name | type name
      values: [value1, value2, ...] | { key1: value1, key2: value2, ...}
      strict: True | False

where 

- ``member name``/``type name`` contains string value of integer variable name for which we want to define enumerated values
- ``[value1, value2, ...]`` is comma-separated list of enumerated values (implicitly numbered, starting from 0) 
- ``{ key1: value1, key2: value2, ...}`` is comma-separated list of key-value pairs, where ``key`` is integer value and ``value`` is it's assigned string value
- ``strict`` is boolean value, which disables warning, if integer does not contain a value specified in the enum list (default ``True``)
    

Example of enums in struct definition contains:
- member named ``weekday`` and values defined as a list of key-value pairs.
- definition of enumerated values for ``int`` type. Values are given by simple list, therefore numbering is implicit (starting from 0, i.e. ``Blue`` = 2). Warning in case of invalid integer value *will* be displayed. ::

    Structs:
      - name: enum_example1
        id: 10
        description: Enum config example
        enums:
          - member: weekday
            values: {1: MONDAY, 2: TUESDAY, 3: WEDNESDAY, 4: THURSDAY, 5: FRIDAY, 6: SATURDAY, 7: SUNDAY}
          - type: int
            values: [Black, Red, Blue, Green, Yellow, White]
            strict: True # Disable warning if not a valid value


Bitstrings
^^^^^^^^^^

It is possible to configure bitstrings in the utility. This makes it possible to view common data types like integer, short, float, etc. used as a bitstring in the wireshark dissector.

There is two ways to configure bitstrings, the first one is to specify a struct member and define the bit representation. The second option is to specify bits for all struct members of a given type.

These rules specifies the config:

- The bits are specified as 0...n, where 0 is the most significant bit
- A bit group can be one or more bits.
- Bit groups have a name
- It is possible to name all possible values in a bit group.


Below, there is an example of a configuration for the member named ``flags`` and all the members of ``short`` type belonging to the struct ``example``. 

- member ``flags``: This example has four bits specified, the first bit group is named "In use" and represent bit 0. The second group represent bit 1 and is named "Endian", and the values are named: 0 = "Big", 1 = "Little". The last group is "Platform" and represent bit 2-3 and have 4 named values.
- type ``short``: Each of the 3 bits represents one colour channel and it can be either "True" or "False".

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
          - type: short
            0: Red
            1: Green
            2: Blue

.. _ids:

Dissector message ID
~~~~~~~~~~~~~~~~~~~~

Every packet with C struct captured by Wireshark contains a header. One of the fields in the header, the ``id`` field, specifies which dissector should be loaded to dissect the actual struct. The value of this field can be specified in the configuration file. 

This is an example of the specification ::

    Structs:
        - name: structname
          id: 10

More different messages can be dissected by one specific dissector. Therefore, the struct configuration can contain a whole list of dissector message ID's, that can process the struct. ::

    Structs:
        - name: structname
          id: [12, 43, 3498]
         
.. note::
    The ``id`` must be an integer between 0 and 65535.


External Lua dissectors
~~~~~~~~~~~~~~~~~~~~~~~

In some cases, CSjark will not be able to deliver the desired result from its own analysis, and the configuration options above may be too constraining. In this case, it is possible to write the lua dissector by hand, either for a given member or for an entire struct. 

More information how to write Lua code can be found in `Lua reference manual  <http://www.lua.org/manual/5.1/>`_.

A custom Lua code for desired struct must be defined in an external conformance file with extension ``.cnf``. The conformance file name and relative path then must be defined in the configuration file for the struct for which is the custom code applied for. The attribute name for the custom Lua definition file and path is ``cnf``, as shown below:

::

    # CSjark configuration file

    Structs:
        - name: custom_lua
          cnf: etc/custom_lua.cnf
          id: 1
          description: example of external custom Lua file definition

Writing the conformance file implies respecting following rules:

- The conformance file (as well as CSjark configuration files) follows YAML_ syntax specification.
- Each section starts with ``#.<SECTION>`` for example ``#.COMMENT``.
- Unknown sections are ignored.

The conformance file implementation allows user to place the custom Lua code on various places within the Lua dissector code already generated by CSjark. There is a list of possible places:

    ====================================    =======================                                                                                                                                                           
    ``DEF_HEADER id``                       Lua code added before a Field defintion.                                                                                                                                          
    ``DEF_BODY id``                         Lua code to replace a Field defintion. Within the definition, the original body can be referenced as ``%(DEFAULT_BODY)s`` or ``{DEFAULT_BODY}``                                   
    ``DEF_FOOTER id``                       Lua code added after a Field defintion                                                                                                                                            
    ``DEF_EXTRA``                           Lua code added after the last defintion                                                                                                                                           
    ``FUNC_HEADER id``                      Lua code added before a Field function code                                                                                                                                       
    ``FUNC_BODY id``                        Lua code to replace a Field function code                                                                                                                                         
    ``FUNC_FOOTER id``                      Lua code added after a Field function code                                                                                                                                        
    ``FUNC_EXTRA``                          Lua code added at end of dissector function                                                                                                                                       
    ``COMMENT``                             A multiline comment section                                                                                                                                                       
    ``END``                                 End of a section                                                                                                                                                                  
    ``END_OF_CNF``                          End of the conformance file                                                                                                                                                       
    ====================================    =======================          
   
Where ``id`` denotes C struct member name (``DEF_*``) or field name (``FUNC_*``).                                                                                                                                                 
                                                                                                                                                                                                                                 
Example of such conformance file follows: ::                                                                                                                                                                                     
                                                                                                                                                                                                                                 
    #.COMMENT
        This is a .cnf file comment section
    #.END
    
    #.DEF_HEADER super
    -- This code will be added above the 'super' field definition
    #.END
    
    #.COMMENT
        DEF_BODY replaces code inside the dissector function.
        Use %(DEFAULT_BODY)s or {DEFAULT_BODY} to use generated code.
    #.DEF_BODY hyper
    -- This is above 'hyper' definition
    %(DEFAULT_BODY)s
    -- This is below 'hyper'
    #.END
    
    #.DEF_FOOTER name
    -- This is below 'name' definition
    #.END
    
    
    #.DEF_EXTRA
    -- This was all the Field defintions
    #.END
    
    
    #.FUNC_HEADER precise
        -- This is above 'precise' inside the dissector function.
    #.END
    
    
    #.COMMENT
        FUNC_BODY replaces code inside the dissector function.
        Use %(DEFAULT_BODY)s or {DEFAULT_BODY} to use generated code.
    #.FUNC_BODY name
        --[[ This comments out the 'name' code
        {DEFAULT_BODY}
        ]]--
    #.END
    
    #.FUNC_FOOTER super
        -- This is below 'super' inside dissector function
    #.END
    
    #.FUNC_EXTRA
        -- This is the last line of the dissector function
    #.END_OF_CNF
    
This conformance file when run with this C header code: ::

    struct custom_lua {
        short normal;
        int super;
        long long hyper;
        
        char name;
        double precise;
    
    };

...will produce this Lua dissector: ::
    
    -- Dissector for win32.custom_lua: custom_lua (Win32)
    local proto_custom_lua = Proto("win32.custom_lua", "custom_lua (Win32)")
    
    -- ProtoField defintions for: custom_lua
    local f = proto_custom_lua.fields
    f.normal = ProtoField.int16("custom_lua.normal", "normal")
    -- This code will be added above the 'super' field definition
    f.super = ProtoField.int32("custom_lua.super", "super")
    -- This is above 'hyper' definition
    f.hyper = ProtoField.int64("custom_lua.hyper", "hyper")
    -- This is below 'hyper'
    f.name = ProtoField.string("custom_lua.name", "name")
    -- This is below 'name' definition
    f.precise = ProtoField.double("custom_lua.precise", "precise")
    -- This was all the field defintions
    
    -- Dissector function for: custom_lua
    function proto_custom_lua.dissector(buffer, pinfo, tree)
        local subtree = tree:add_le(proto_custom_lua, buffer())
        if pinfo.private.caller_def_name then
            subtree:set_text(pinfo.private.caller_def_name .. ": " .. proto_custom_lua.description)
            pinfo.private.caller_def_name = nil
        else
            pinfo.cols.info:append(" (" .. proto_custom_lua.description .. ")")
        end
    
        subtree:add_le(f.normal, buffer(0, 2))
        subtree:add_le(f.super, buffer(4, 4))
        -- This is below 'super' inside dissector function
        subtree:add_le(f.hyper, buffer(8, 8))
        --[[ This comments out the 'name' code
            subtree:add_le(f.name, buffer(16, 1))
        ]]--
        -- This is above 'precise' inside the dissector function.
        subtree:add_le(f.precise, buffer(24, 8))
        -- This is the last line of the dissector function
    end
    
    delegator_register_proto(proto_custom_lua, "Win32", "custom_lua", 1)
          
Support for Offset and Value in Lua Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Via `External Lua dissectors`_ CSjark also provides a way to add new proto fields to the dissector in Wireshark, with correct offset value and correct Lua variable.

To access the fields value and offset, ``{OFFSET}`` and ``{VALUE}`` strings may be put into the conformance file as shown below: ::

    #.FUNC_FOOTER pointer
        -- Offset: {OFFSET}
        -- Field value stored in lua variable: {VALUE}
    #.END

Adding the offset and variable value is only possible in the parts that change the code of Lua functions, i.e. ``FUNC_HEADER``, ``FUNC_BODY`` and ``FUNC_FOOTER``.

Above listed example leads to following Lua code: ::
    
    local field_value_var = subtree:add(f.pointer, buffer(56,4))
        -- Offset: 56
        -- Field value stored in lua variable: field_value_var
        
.. note::
    The value of the referenced variable can be used after it is defined.
            

Trailers
~~~~~~~~

CSjark only creates dissectors from C structs defined as its input. To be able to use built-in dissectors in Wireshark, it is necessary to configure it. Wireshark has more than 1000 built-in dissectors. Several trailers can be configured for a packet.

The following parameters are allowed in trailers:

    ======  =======
    name    Protocol name for the built-in dissector
    count   The number of trailers
    member  Struct member, that contain the amount of trailers
    size    Size of the buffer to feed to the protocol
    ======  =======

There are two ways to configure the trailers - specify the total number of trailers or give a variable in the struct, which contains the amount of trailers. Both ways to configure trailers are shown below. In case the variable ``trailer_count`` equals 2, the definitions has the same effect. ::

    trailers:
      - name: proto1
        member: trailer_count
        size: 32
      
    trailers:
      - name: proto1
        count: 2
        size: 32

Example:
The example below shows an example with BER [#]_, which has 4 trailers with a size of 6 bytes.

.. [#] Basic Encoding Rules

::

    trailers:
      - name: ber
      - count: 4
      - size: 6


Custom handling of data types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The utility supports custom handling of specified data types. Some variables in input C header may actually represent other values than its own type. This CSjark feature allows user to map types defined in C header to Wireshark field types. Also, it provides a method to change how the input field is displayed in Wireshark. The custom handling must be done through a configuration file.

For example, this functionality can cause Wireshark to display ``time_t`` data type as ``absolute_time``. The displayed type is given by generated Lua dissector and functions of ``ProtoField`` class.

List of available output types follows:

``Integer types``
    uint8, uint16, uint24, uint32, uint64, int8, int16, int24, int32, int64, framenum

``Other types``
    float, double, string, stringz, bytes, bool, ipv4, ipv6, ether, oid, guid, absolute_time, relative_time
    
For ``Integer`` types, there are some specific attributes that can be defined (see below_). More about each individual type can be found in `Wireshark reference`_.

.. _Wireshark reference: http://www.wireshark.org/docs/wsug_html_chunked/lua_module_Proto.html#lua_class_ProtoField 


The section name in configuration file for custom data type handling is called ``customs``. This section can contain following attributes:

- Required attributes
    
    =====================   ============
    Attribute name          Value
    =====================   ============
    ``member`` | ``type``   Name of member or type for which is the configuration applied
    ``field``               Displayed type (see above)
    =====================   ============
    
- Optional attributes - all types
    
    ===============     ============
    Attribute name      Value
    ===============     ============
    ``abbr``            Filter name of the field (the string that is used in filters)
    ``name``            Actual name of the field
    ``desc``            The description of the field (displayed on Wireshark statusbar)
    ===============     ============

.. _below:
    
- Optional attributes - Integer types only:
    
    ==================     ============
    Attribute name         Value
    ==================     ============
    ``base``               Displayed representation - can be one of ``base.DEC``, ``base.HEX`` or ``base.OCT``
    ``values``             List of ``key:value`` pairs representing the Integer value - e.g. ``{0: Monday, 1: Tuesday}``
    ``mask``               Integer mask of this field    
    ==================     ============

Example of such a configuration file follows: ::

    Structs:
      - name: custom_type_handling
        id: 1
        customs:
          - type: time_t
            field: absolute_time
          - member: day
            field: uint32
            abbr: day.name
            name: Weekday name
            base: base.DEC
            values: { 0: Monday, 1: Tuesday, 2: Wednesday, 3: Thursday, 4: Friday}
            mask: nil
            desc: This day you will work a lot!!
            
and applies for example for this C header file: ::

    #include <time.h>
    
    struct custom_type_handling {
        time_t abs;
        int day;
    };

Both struct members are redefined. First will be displayed as ``absolute_type`` according to its type (``time_t``), second one is changed because of the struct member name (``day``).

Unknown structs handling
~~~~~~~~~~~~~~~~~~~~~~~~

The header files that the utility parses, may have nested struct that is not defined in any other header file. To make  it possible to generate a dissector for this case, the user must be able to specify the size of the struct in a configuration file. When the sizes are specified it will be possible to generate a struct that can display the defined members of the struct correctly in the utility, for the parts that are not defined only the hex value will be displayed. This feature is added as a possible way to solve include dependencies that our utility is not able to solve. The user of the utility will get an error message when the utility is not able to find include dependencies, and the user may add the size of struct to be able to generate a dissector for the struct.

The size of unknown struct may be defined directly in the struct configuration as ``size`` attribute, similar to the example below: ::

    Structs:
        - name: unknown struct
          id: 111
          size: 78

.. note::
    Size must be defined as a positive integer (or 0).

Options Configuration
---------------------

CSjark processing behaviour can be set up in various ways. Besides letting the user to specify how the CSjark should work by the command line arguments (see section :ref:`use`), it is also possible to define the options as a part of the configuration file(s). 

=========================   ==============  =============================   ==========================
Configuration file field    CLI equivalent  Value                           Description
=========================   ==============  =============================   ==========================
``verbose``                 ``-v``          ``True``/``False``              Print detailed information
``debug``                   ``-d``          ``True``/``False``              Print debugging information
``strict``                  ``-s``          ``True``/``False``              Only generate dissectors for known structs
``output_dir``              ``-o``          ``None`` or path                Definition of output destination
``output_file``             ``-o``          ``None`` or file name           Writes the output to the specified file
``generate_placeholders``   ``-p``          ``True``/``False``              Generate placeholder config file for unknown structs
``use_cpp``                 ``-n``          ``True``/``False``              Enables/disables the C pre-processor
``cpp_path``                ``-C``          ``None`` or file name           Specifies which preprocessor to use  
``excludes``                ``-x``          List of excluded paths          File or folders to exclude from parsing
``platforms``                               List of platform names          Set of platforms to support in dissectors
``include_dirs``            ``-I``          List of directories             Directories to be searched for Cpp includes
``includes``                ``-i``          List of includes                Process file as Cpp #include "file" directive
``defines``                 ``-D``          List of defines                 Predefine name as a Cpp macro
``undefines``               ``-U``          List of undefines               Cancel any previous Cpp definition of name
``arguments``               ``-A``          List of additional arguments    Any additional C preprocessor arguments
=========================   ==============  =============================   ==========================

The last 5 options can be also specified separately for each individual input C header file. This can be achieved by adding sequence ``files`` with mandatory attribute ``name``. 

Below you can see an example of such ``Options`` section: ::

    Options:
        verbose: True
        debug: False
        strict: False
        output_dir: ../out
        output_file: output.log
        generate_placeholders: False
        use_cpp: True
        cpp_path: ../utils/cpp.exe
        excludes: [examples, test]
        platforms: [default, Win32, Win64, Solaris-sparc, Linux-x86]
        include_dirs: [../more_includes]
        includes: [foo.h, bar.h]
        defines: [CONFIG_DEFINED=3, REMOVE=1]
        undefines: [REMOVE]
        arguments: [-D ARR=2]
        files:
          - name: a.h
            includes: [b.h, c.h]
            define: [MY_DEFINE]

.. note::
    If you give CSjark multiple configuration files with the same values defined, it takes:
    
    - for attributes with single value: a value from *last processed config file* is valid
    - for attributes with list values: lists are *merged*



Platform specific configuration
-------------------------------

To ensure that CSjark is usable as much as possible, platform specific


Entire platform setup is done via Python code, specifically ``platform.py``. This file contains following sections:

1. Platform class definition including it's methods
2. Default mapping of C type and their wireshark field type
3. Default C type size in bytes
4. Default alignment size in bytes
5. Custom C type sizes for every platform which differ from default
6. Custom alignment sizes for every platform which differ from default
7. Platform-specific C preprocessor macros
8. Platform registration method and calling for each platform

      
When defining new platform, following steps should be done. Referenced sections apply to ``platform.py`` sections listed above. All the new dictionary variables should have proper syntax of `Python dictionary <http://docs.python.org/release/3.1.3/tutorial/datastructures.html#dictionaries>`_:

**Field sizes**
    Define custom C type sizes in section 5. Create new dictionary with name in capital letters. Only those different from default (section 3) must be defined. 

    ::
        
        NEW_PLATFORM_C_SIZE_MAP = {
            'unsigned long': 8,
            'unsigned long int': 8,
            'long double': 16
        }

**Memory alignment**    
    Define custom memory alignment sizes in section 6. Create new dictionary with name in capital letters. Only those different from default (section 4) must be defined. 
    
    ::
    
        NEW_PLATFORM_C_ALIGNMENT_MAP = {
            'unsigned long': 8,
            'unsigned long int': 8,
            'long double': 16
        }
     
**Macros**
    Define dictionary of platform specific macros in section 7. These macros then can be used within C header files to define platform specific struct members etc. E.g.: 
    
    ::
   
        #if _WIN32
            float num;
        #elif __sparc
            long double num;
        #else
            double num;


    Example of such macros: 
    
    ::
     
        NEW_PLATFORM_MACROS = {
            '__new_platform__': 1, '__new_platform': 1
        }


**Register platform**
    In last section (8), the new platform must be registered. Basically, it means calling the constructor of Platform class. That has following parameters:
    
    ::
        
        Platform(name, flag, endian, macros=None, sizes=None, alignment=None)    

    where

    =========== ===
    ``name``    name of the platform
    ``flag``    unique integer value representing this platform
    ``endian``  either ``Platform.big`` or ``Platform.little``
    ``macros``  C preprocessor platform-specific macros like _WIN32
    ``sizes``   dictionary which maps C types to their size in bytes
    =========== ===    
 
    Registering of the platform then might look as follows: ::
    
        # New platform
        Platform('New-platform', 8, Platform.little,
                 macros=NEW_PLATFORM_MACROS,
                 sizes=NEW_PLATFORM_C_SIZE_MAP,
                 alignment=NEW_PLATFORM_C_ALIGNMENT_MAP)




.. _YAML: http://www.yaml.org/
