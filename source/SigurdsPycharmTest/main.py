from Test import TestClass
from Test import NameList

__author__ = 'Sigurd'

def main():
    print("Hello world!")
    testclass = TestClass()
    testclass.printHelloWorld()

    nameList = NameList()
    nameList.addName("Thales")
    nameList.addName("PyCharm")
    nameList.addName("Microsoft")

    nameList.printNames()


main()