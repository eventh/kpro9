============
Using CSjark
============

CSjark can be invoked by running the ``csjark.py`` script. The arguments must be specified according to: ::

    csjark.py [-h] [-verbose] [-debug] [-nocpp]
              [-Include [include [include ...]]]
              [-input [header [header ...]]]
              [-config [config [config ...]]]
              [-output [output]]
              [header] [config]

The arguments here specify the following:

``header``
  a c header file to parse.
``config``
  a configuration file to parse.


**Optional arguments:**

  -h, --help            		 Show a help message and exit.
  -v, --verbose                  Print detailed information.
  -d, --debug              		 Print debugging information.
  -n, --nocpp              		 Disables the C pre-processor.
  -I include_list, --Include=include_list        C preprocessor includes
  -i header_list, --input=header_list      		 Specifies that CSjark should look for struct definitions in the ``header`` files.
  -c config_list, --config=config_list           Specifies that the program should use the ``config`` files as configuration.
  -o output, --output=output         		     Writes the output to the specified file ``output``.


**Example usage:** ::

    python csjark.py -v headerfile.h configfile.yml

