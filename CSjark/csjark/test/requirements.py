"""
Module for white-box testing the specific customer requirements.
"""
import sys, os
from attest import Tests, assert_hook, contexts
from pycparser import c_ast

try:
    import cparser
    import config
except ImportError:
    # If cparser is not installed, look in parent folder
    sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '../'))
    import cparser
    import config


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
    ast = cparser.parse('enum c {a, b=3}; struct req { enum c test; };')
    assert isinstance(_child(ast.children()[1], 4), c_ast.Enum)
    enum = cparser.find_structs(ast)[0].fields[0]
    assert enum
    assert enum.name == 'test'
    assert enum.values == '{[0]="a", [3]="b"}'
    assert enum.type == 'uint32' and enum.size == 4

# FR1-C: The utility must support members of type struct
@parse_structs.test
def req_1c():
    """Test requirement FR1-C: Support member of type struct."""
    a = cparser.parse('''
    struct outside { struct inside { int a; char b; }; };
    ''')
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
    ast = cparser.parse('struct req {int a[9][8]; char b[30]; float c[10];};')
    a, b, c = [_child(i, 1) for i in _child(ast, 2).children()]
    assert isinstance(b, c_ast.ArrayDecl) and isinstance(c, c_ast.ArrayDecl)
    assert isinstance(_child(a, 1), c_ast.ArrayDecl)
    assert _child(a, 2).declname == 'a'
    assert _child(a, 3).names[0] == 'int'
    fields = cparser.find_structs(ast)[0].fields
    # TODO: test that fields are correct

# FR1-F: The utility should detect structs with the same name
@parse_structs.test
def req_1f():
    """Test requirement FR1-F: Detect same name structs."""
    code = 'struct a {int c;}; struct b { int d; struct a {int d;}; };'
    ast = cparser.parse(code, 'test')
    with contexts.raises(cparser.ParseError) as error:
        cparser.find_structs(ast)
    assert str(error).startswith('Two structs with same name: a')


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
cpp = Tests()

@cpp.context
def create_ast():
    """Parse a C headerfile with C preprocessor, and create an AST."""
    # Find the header files and cpp if we are run from a different folder
    if __name__ == '__main__':
        path = os.path.dirname(sys.argv[0])
    else:
        path = os.path.dirname(__file__)

    cpp_h = os.path.join(path, 'cpp.h')
    inc_h = os.path.join(path, 'include.h')
    cpp_path = os.path.join(path, '../../utils/cpp.exe') # Tmp hack

    assert os.path.isfile(cpp_h) and os.path.isfile(inc_h)
    ast = cparser.parse_file(cpp_h, cpp_path=cpp_path)
    yield ast

# FR3-A: The utility shall support #include
@cpp.test
def req_3a(ast):
    """Test requirement FR3-A: Support for #include."""
    assert ast
    a, b, c = ast.children()
    assert _child(c, 5).names[0] == 'bool'
    assert int(_child(c, 3).children()[1].value) == 5

# FR3-B: The utility shall support #define and #if
@cpp.test
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
@cpp.test
def req_3c(ast):
    """Test requirement FR3-C: Support for platform specific macros."""
    pass #TODO


# Tests for the fourth requirement, support configuration
# FR4: The utility must support user configuration
configuration = Tests()

@configuration.context
def create_rules():
    text = '''
    Structs:
      - name: one
        id: 9
        description: a struct
      - name: two
        id: 11

    RangeRules:
      - struct: one
        member: percent
        min: 10
        max: 30
      - struct: two
        type: int
        max: 15.5
    '''
    config.parse_file('test', only_text=text)
    yield config.StructConfig.find('one'), config.StructConfig.find('two')
    del config.StructConfig.configs['one']
    del config.StructConfig.configs['two']

# FR4-A: Configuration must support valid ranges for struct members
@configuration.test
def req4_a(one, two):
    assert one and two
    rule, = one.get_rules('percent', None)
    assert rule.max == 30 and rule.min == 10
    rule, = two.get_rules('holy hand grenade', 'int')
    assert rule.max == 15.5 and rule.min is None

# FR4-B: Configuration must support custom Lua files for specific protocols
# FR4-C: Configuration must support custom handling of specific data types

# FR4-D: Configuration must support specifying the ID of dissectors
@configuration.test
def req4_d(one, two):
    assert one and two
    assert one.id == 9 and two.id == 11
    assert one.description == 'a struct' and two.description is None

# FR4-E: Configuration must support various trailers
# FR4-F: Configuration must support integers which represent enums
# FR4-G: Configuration must support members which are bit string


# Tests for the fifth requirement, support endian etc
# FR5: Handle binary input which size and endian differs
# FR5-A: Flags must be specified in configuration for each platform
# FR5-B: Flags within message headers should signal the platform
# FR5-C: Generate dissectors which support both little and big endian
# FR5-D: Generate dissectors which support different sizes depending


# Tests for the sixth requirement, support command line interface
# FR6: The utility shall support parameters from command line
# FR6-A: Command line shall support parameter for C header file
# FR6-B: Command line shall support parameter for configuration file
# FR6-C: Command line shall support batch mode of C header and config files
# FR6-D: In batch mode, don't regenerate dissectors which aren't modified


if __name__ == '__main__':
    all_tests = Tests([parse_structs, cpp, configuration])
    all_tests.run()

