from source.SigurdsPycharmTest.nameList import NameList

__author__ = 'Sigurd'

def main():
    testClass = TestClass(2, 4)
    testClass.printAdd()
    testClass.printSub()

    nameList = NameList()
    nameList.addName("Thales")
    nameList.addName("Microsoft")
    nameList.addName("PyCharm")
    nameList.printNames()

class TestClass:
    def __int__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2

        def printAdd(self):
            print(self.number1 + self.number2)

        def printSub(self):
            print(self.number1 - self.number2)



main()