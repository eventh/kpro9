import configuration

class ConfigError(Exception):
    pass

class RangeRule():
    def __init__(self, file, struct, member, type, minvalue, maxvalue):
        self.file = file
        self.struct = struct
        self.member = member
        
    def setType(self, type):
        if type in Configuration.ValidRangeType:
            self.type = type
        else:
            raise ConfigError()

    def __convert(value):
        try:
            value = int(value)
        except AttributeError:
            try:
                value = float(value)
            except AttributeError:
                raise ConfigError()
                    
        return value
    
    def setMinvalue(self, minvalue):
        self.minvalue = __convert(minvalue)
    
    def setMaxValue(self, maxvalue):
        self.maxvalue = __convert(maxvalue)
            