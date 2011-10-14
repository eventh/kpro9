=============
 Limitations
=============

CSjark does not support pointer types, because the pointer values are no longer relevant on a different computer with a different memory layout.

CSjark currently have no way of specifying different type sizes or endian for different platform, and will therefore only produce correct dissector for a platform that conforms with our default values and communicates with a computer with the same endian and type sizes.

There are currently no support for typedef types.