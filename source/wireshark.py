
class BaseProtoField:
    def __init__(self, abbr, name=None, desc=None):
        self.abbr = abbr
        self.name = name
        self.desc = desc

    def get_args(self):
        return [self.abbr, self.name, self.desc]

    def create_lua(self):
        args = ', '.join([str(i) for i in self.get_args() if i is not None])
        return 'ProtoField.%s (%s)' % (self.__class__.__name__, args)

class IntProtoField(BaseProtoField):
    def __init__(self, abbr, name=None, desc=None,
            base=None, valuestring=None, mask=None):
        super().__init__(self, abbr, name, desc)
        self.base = base
        self.valuestring = valuestring
        self.mask = mask

    def get_args(self):
        return [self.abbr, self.name, self.desc,
                self.base, self.valuestring, self.mask]

# ProtoField specifies something, for adding items to the three
INT_TYPES = ["uint8", "uint16", "uint24", "uint32", "uint64", "framenum"]
OTHER_TYPES = ["float", "double", "string", "stringz", "bytes",
                "bool", "ipv4", "ipv6", "ether", "oid", "guid"]

# Create classes for all the protofield types, HACK!
TYPES_MAPPING = {}
for field_type in INT_TYPES:
    exec('class %s(IntProtoField): pass' % field_type)
    TYPES_MAPPING[field_type] = eval(field_type)
for field_type in OTHER_TYPES:
    exec('class %s(BaseProtoField): pass' % field_type)
    TYPES_MAPPING[field_type] = eval(field_type)

