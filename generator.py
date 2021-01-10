import random


class generateListOfPages:
    def __init__(self, numberOfPages,pagesRange):
        self.numberOfPages = numberOfPages
        self.listOfPages = []
        self.pagesRange=pagesRange
        for counter in range(0, numberOfPages):
            self.listOfPages.append(random.randint(1,self.pagesRange))

    def viewPages(self):
        for i in range(0, self.numberOfPages):
            print("i :", self.listOfPages[i])

    def saveListOfPages(self, fileName):
        try:
            file = open(fileName, 'w')
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        for i in range(0, self.numberOfPages):
            file.write(str(self.listOfPages[i]))
            file.write('\n')
        try:
            file.close()
        except Exception as exc:
            print("Nie mozna zamknac pliku:", exc)

    def loadListOfPages(self, fileName):
        try:
            with open(fileName) as file:
                listOfLines = file.read().splitlines()
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        for i in range(0, len(listOfLines)):
            self.listOfPages[i] = listOfLines[i]
        try:
            file.close()
        except Exception as exc:
            print("Nie mozna zamknac pliku:", exc)


