"""
Module for white-box testing the specific customer requirements.
"""
import sys, os
from attest import Tests, assert_hook, contexts
from pycparser import c_ast

import cpp
import csjark
import cparser
import dissector
import config
from config import Options


def _child(node, depth=1):
    """Find a child in the AST, by depth first."""
    child = node
    while depth > 0:
        child = child.children()[0]
        depth -= 1
    return child


# Tests for the first requirement, parsing of basic C structs
# FR1: The utility must be able to read basic C language
#      struct definitions from C header files
parse_structs = Tests()

# FR1-A: The utility must support the following basic
#        data types: int, float, char and boolean
@parse_structs.test
def req_1a():
    """Test requirement FR1-A: Support for int, floa, char and bool."""
    ast = cparser.parse('''
    struct basic { int a; float b; char c; _Bool d; };
    ''')
    a, b, c, d = _child(ast, 2).children()
    assert _child(a, 2).names[0] == 'int'
    assert _child(b, 2).names[0] == 'float'
    assert _child(c, 2).names[0] == 'char'
    assert _child(d, 2).names[0] == '_Bool'

# FR1-B: The utility must support members of type enum
@parse_structs.test
def req_1b():
    """Test requirement FR1-B: Support enums."""
    cparser.StructVisitor.all_protocols = {}
    ast = cparser.parse('enum c {a, b=3}; struct req { enum c test; };')
    assert isinstance(_child(ast.children()[1], 4), c_ast.Enum)
    enum = list(cparser.find_structs(ast)[0].dissectors.values())[0].children[0]
    assert enum
    assert enum.name == 'test'
    assert enum._valuestring_values == '{[0]="a", [3]="b"}'
    assert enum.type == 'uint32' and enum.size == 4

# FR1-C: The utility must support members of type struct
@parse_structs.test
def req_1c():
    """Test requirement FR1-C: Support member of type struct."""
    a = cparser.parse('struct outside { struct inside { int a; char b; }; };')
    assert isinstance(_child(a, 4), c_ast.Struct)
    assert _child(a, 2).name == 'outside' and _child(a, 4).name == 'inside'
    assert _child(a, 7).names[0] == 'int'

# FR1-D: The utility must support members of type union
@parse_structs.test
def req_1d():
    """Test requirement FR1-D: Support unions."""
    ast = cparser.parse('struct req { union type { int a; char b; }; };')
    assert isinstance(_child(ast, 4), c_ast.Union)
    assert _child(ast, 4).name == 'type'

# FR1-E: The utility must support members of type array
@parse_structs.test
def req_1e():
    """Test requirement FR1-E: Support arrays."""
    cparser.StructVisitor.all_protocols = {}
    ast = cparser.parse('struct req1e {int a[8][7]; char b[9]; float c[5];};')
    a, b, c = [_child(i, 1) for i in _child(ast, 2).children()]
    assert isinstance(b, c_ast.ArrayDecl) and isinstance(c, c_ast.ArrayDecl)
    assert isinstance(_child(a, 1), c_ast.ArrayDecl)
    assert _child(a, 2).declname == 'a'
    assert _child(a, 3).names[0] == 'int'
    a, b, c = list(cparser.find_structs(ast)[0].dissectors.values())[0].children
    assert isinstance(b, dissector.Field)
    assert a.type == 'bytes' and b.type == 'string' and c.type == 'bytes'
    assert a.size == 4*56 and b.size == 9 and c.size == 20

# FR1-F: The utility should detect structs with the same name
@parse_structs.test
def req_1f():
    """Test requirement FR1-F: Detect same name structs."""
    cparser.StructVisitor.all_protocols = {}
    code = 'struct a {int c;};\nstruct b { int d;\nstruct a {int d;}; };'
    ast = cparser.parse(code, 'test')
    with contexts.raises(cparser.ParseError) as error:
        cparser.find_structs(ast)
    assert str(error).startswith('Two structs with same name a')
    cparser.StructVisitor.all_protocols = {}


# Tests for the second requirement, generate dissectors in lua
# FR2: The utility must be able to generate lua dissectors for
#      the binary representation of C struct
# FR2-A: The dissector shall be able to display simple structs
# FR2-B: The dissector shall be able to support structs within structs
# FR2-C: The dissector must support Wiresharks built-in
#        filter and search on attributes
# FR2-D: The dissector shall be able to recognize invalid
#        values for a struct member
# Probably best to implement these later!


# Tests for the third requirement, C preprocessor directives and macros
# FR3: The utility must support C preprocessor directives and macros
cpps = Tests()

@cpps.context
def create_ast():
    """Parse a C headerfile with C preprocessor, and create an AST."""
    # Find the header files and cpp if we are run from a different folder
    cpp_h = os.path.join(os.path.dirname(__file__), 'cpp.h')
    inc_h = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(cpp_h) and os.path.isfile(inc_h)
    text = cpp.parse_file(cpp_h)
    yield cparser.parse(text)

# FR3-A: The utility shall support #include
@cpps.test
def req_3a(ast):
    """Test requirement FR3-A: Support for #include."""
    assert ast
    a, b, c = ast.children()
    assert _child(c, 5).names[0] == 'bool'
    assert int(_child(c, 3).children()[1].value) == 5

# FR3-B: The utility shall support #define and #if
@cpps.test
def req_3b(ast):
    """Test requirement FR3-B: Support for #define and #if."""
    a, b, c = ast.children()
    assert _child(b, 1).name == 'simple'
    assert _child(b, 2).name == 'arr'
    assert isinstance(_child(b, 3), c_ast.ArrayDecl)
    type_decl, constant = _child(b, 3).children()
    assert constant.type == 'int'
    assert int(constant.value) == 10

# FR3-C: Support WIN32, _WIN32, _WIN64, __sparc__, __sparc and sun
@cpps.test
def req_3c(ast):
    """Test requirement FR3-C: Support for platform specific macros."""
    pass #TODO


# Tests for the fourth requirement, support configuration
# FR4: The utility must support user configuration
configuration = Tests()

@configuration.context
def create_rules():
    """Create configuration for different rules."""
    text = '''
    Structs:
      - name: one
        id: 9
        description: a struct
        ranges:
          - member: percent
            min: 10
            max: 30
        bitstrings:
          - member: flags
            1: Test
            2: [Flag, A, B]
        customs:
          - member: abs
            field: absolute_time
        trailers:
          - name: ber
            member: asn1_count
            size: 12
          - name: ber
            count: 1
      - name: two
        id: [11, 12, 13, 14]
        ranges:
          - type: int
            max: 15.5
        bitstrings:
          - type: short
            1-3: [Short, A, B, C, D, E, F, G, H]
            4: [Nih]
        customs:
          - type: BOOL
            field: bool
            size: 4
            abbr: bool
            name: A BOOL
        trailers:
          - name: ber
            count: 3
            size: 8
    '''
    config.parse_file('test', only_text=text)
    yield Options.configs['one'], Options.configs['two']
    Options.configs = {}

# FR4-A: Configuration must support valid ranges for struct members
@configuration.test
def req4_a(one, two):
    """Test requirement FR4-A: Configuration of valid ranges."""
    assert one and two
    rule, = one.get_rules('percent', None)
    assert rule.max == 30 and rule.min == 10
    rule, = two.get_rules('holy hand grenade', 'int')
    assert rule.max == 15.5 and rule.min is None

# FR4-B: Configuration must support custom Lua files for specific protocols


# FR4-C: Configuration must support custom handling of specific data types
@configuration.test
def req4_c(one, two):
    """Test requirement FR4-C: Custom handling of specific data types."""
    rule, = one.get_rules('abs', 'short')
    assert rule.field == 'absolute_time'
    assert rule.size is None and rule.abbr is None
    rule, = two.get_rules(None, 'BOOL')
    assert rule.field == 'bool' and rule.size == 4
    assert rule.abbr == 'bool' and rule.name == 'A BOOL'

# FR4-D: Configuration must support specifying the ID of dissectors
@configuration.test
def req4_d(one, two):
    """Test requirement FR4-D: Configuration of dissector ID."""
    assert one and two
    assert one.id == [9] and two.id == [11, 12, 13, 14]
    assert one.description == 'a struct' and two.description is None

# FR4-E: Configuration must support various trailers
@configuration.test
def req4_e(one, two):
    """Test requirement FR4-E: Configuration of trailers."""
    a, b, c = one.trailers + two.trailers
    assert a.name == 'ber' and b.name == 'ber' and c.name == 'ber'
    assert c.count == 3 and a.count is None and b.count == 1
    assert a.member == 'asn1_count' and c.member is None
    assert c.size == 8 and a.size == 12 and b.size is None

# FR4-F: Configuration must support integers which represent enums


# FR4-G: Configuration must support members which are bit string
@configuration.test
def req4_g(one, two):
    """Test requirement FR4-G: Configuration of bit strings."""
    one, = one.get_rules('flags', 'int')
    two, = two.get_rules(None, 'short')
    assert one and two
    assert len(one.bits[0]) == 4
    assert one.bits[1][2] == 'Flag'
    assert one.bits[1][3] == {0: 'A', 1: 'B'}
    assert one.bits[0][0] == 1 and one.bits[0][1] == 1
    assert len(two.bits[0][3]) == 8
    assert two.bits[1][2] == 'Nih'
    assert two.bits[1][3] == {0: 'No', 1: 'Yes'}
    assert two.bits[0][0] == 1 and two.bits[0][1] == 3


# Tests for the fifth requirement, support endian etc
# FR5: Handle binary input which size and endian differs
# FR5-A: Flags must be specified in configuration for each platform
# FR5-B: Flags within message headers should signal the platform
# FR5-C: Generate dissectors which support both little and big endian
# FR5-D: Generate dissectors which support different sizes depending


# Tests for the sixth requirement, support command line interface
# FR6: The utility shall support parameters from command line
cli = Tests()

@cli.context
def create_cli():
    """Create Cli as a context to reset it afterwards."""
    c = Options
    defaults = c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file
    yield Options
    c.verbose, c.debug, c.use_cpp, c.output_dir, c.output_file = defaults

# FR6-A: Command line shall support parameter for C header file
@cli.test
def req6_a(cli):
    """Test requirement FR6-A: Parameter for C header file."""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    assert os.path.isfile(include)
    headers, _ = csjark.parse_args([header, '-v', '-d', '-f', include])
    assert len(headers) == 2

# FR6-B: Command line shall support parameter for configuration file
@cli.test
def req6_b(cli):
    """Test requirement FR6-B: Parameter for configuration file."""
    header = os.path.join(os.path.dirname(__file__), 'cpp.h')
    include = os.path.join(os.path.dirname(__file__), 'include.h')
    config = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
    assert os.path.isfile(config)
    headers, configs = csjark.parse_args(
            [header, '--verbose', '-d', '-f', include, '--config', config])
    assert len(headers) == 2

# FR6-C: Command line shall support batch mode of C header and config files
@cli.test
def req6_c(cli):
    """Test requirement FR6-C: Parameters for batch processing."""
    test_folder = os.path.dirname(__file__)
    headers, configs = csjark.parse_args([test_folder])
    assert len(headers) > 0 # Requires that test folder has header files

# FR6-D: In batch mode, don't regenerate dissectors which aren't modified

