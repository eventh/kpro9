__author__ = 'Sigurd'

class TestClass:
    def printHelloWorld(self):
        print("Hello world")

class NameList:
    def __init__(self):
        self.nameList = list()

    def addName(self, name):
        self.nameList.append(name)

    def printNames(self):
        for name in self.nameList:
            print(name)

  