__author__ = 'Sigurd'

class NameList:

    def __init__(self):
        self.nameList = list()

    def addName(self, name):
        self.nameList.__add__(name)

    def printNames(self):
        for name in self.nameList:
            print(name)