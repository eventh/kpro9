============
Using CSjark
============

CSjark can be invoked by running the ``csjark.py`` script. The arguments must be specified according to: ::

    csjark.py [-h] [-verbose] [-debug] [-nocpp]
              [-input [header [header ...]]]
              [-config [config [config ...]]] [-output [output]]
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
  -i header_list, --input=header_list      		 Specifies that CSjark should look for struct definitions in the ``header`` files.
  -c config_list, --config=config_list           Specifies that the program should use the ``config`` files as configuration.
  -o output, --output=output         		     Writes the output to the specified file ``output``.


**Example usage:** ::

    python csjark.py -v -nocpp headerfile.h configfile.yml


**Batch processing of header- and config-files:**
CSjark support batch processing of input files: header- and config-files. The utility can process multiple files without manual intervention. When the utility is provided with arguments, the header and config fields are checked by the Command Line Interface if they are single files or a directory. If single files are provided, the utility will parse these. If a directory is provided, the utility iterates through that directory including all valid header- and config-files. If there are directories inside the provided directory, they are included and handled recursive.
