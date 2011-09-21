import yaml
from RangeRule import RangeRule

def ReadFile(filename):
    stream = open(filename, 'r')
    config = yaml.load(stream)
    rules = []
    
    print(config.keys())
    
    for i in range(len(config['RangeRule'])):
        b = RangeRule(0,0,0)
        a = RangeRule(config['RangeRule'][i]['file'], config['RangeRule'][i]['struct'], config['RangeRule'][i]['member'])
        a.setType(config['RangeRule'][i]['type'])
        a.setMinvalue(config['RangeRule'][i]['minvalue'])
        a.setMaxvalue(config['RangeRule'][i]['maxvalue'])
        rules.append(a)
        print("123")

ReadFile('configuration/example.yml')