=============
 Limitations
=============

CSjark currently have no way of specifying different type sizes or endian for different platform, and will therefore only produce correct dissector for a platform that conforms with our default values and communicates with a computer with the same endian and type sizes.

There are currently no support for typedef types except structs.

CSjark does not yet support struct members of type long double, as Wireshark does not support it.

