import yaml
import RangeRule

def ReadFile(filename):
    stream = file('configuration/example.yml', 'r')
    config = yaml.load(stream)
    rules = []
    
    config.keys()
    
    for i in range(len(config['RangeRule'])):
        a = RangeRule(config['RangeRule'][i]['file'], config['RangeRule'][i]['struct'], config['RangeRule'][i]['member'])
        a.setType(config['RangeRule'][i]['type'])
        a.setMinvalue(config['RangeRule'][i]['minvalue'])
        a.setMaxvalue(config['RangeRule'][i]['maxvalue'])
        rules.append(a)
        print("123")

ReadFile("aead")  