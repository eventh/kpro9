ValidRangeType = ['short', 'short int', 'signed short int', 'unsigned short int', 'int', 'signed int', 'unsigned int', 'long', 'long int', 
'signed long int', 'unsigned long int', 'long long', 'long long int', 'signed long long int', 'unsigned long long int', 'float', 'double',
        'long double']

class ConfigError(Exception):
    pass

class RangeRule():
    def __init__(self, file, struct, member):
        self.file = file
        self.struct = struct
        self.member = member
        
    def setType(self, type):
        if type in ValidRangeType:
            self.type = type
        else:
            raise ConfigError()

    def _convert(self, value):
        try:
            value = int(value)
        except AttributeError:
            try:
                value = float(value)
            except AttributeError:
                raise ConfigError()
                    
        return value
    
    def setMinvalue(self, minvalue):
        self.minvalue = self._convert(minvalue)
    
    def setMaxvalue(self, maxvalue):
        self.maxvalue = self._convert(maxvalue)
            