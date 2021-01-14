import random


class generateListOfPages: #klasa która generuje strony zapisuje je do pliku  i wczytuje z pliku
    def __init__(self, numberOfPages, pagesRange):  # tworze liste stron które będą wchodzić do ramki
        self.numberOfPages = numberOfPages
        self.listOfPages = []
        self.pagesRange = pagesRange
        for counter in range(0, numberOfPages):
            self.listOfPages.append(random.randint(0, self.pagesRange))

    def viewPages(self):  # wyswietla liste stron
        for i in range(0, self.numberOfPages):
            print("i :", self.listOfPages[i])

    def saveListOfPages(self, fileName):  # zapisuje liste stron
        try:
            file = open(fileName,
                        'w')  # otwieram plik o podanej nazwie w argumencie funkcji. Plik ten sie tworzy jeśli nie ma go i czyści
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        for i in range(0, self.numberOfPages):
            file.write(str(self.listOfPages[i]))  # zapisuje odpowiedno do pliku liste stron oddzielając je nową linią
            file.write('\n')

        file.close()  # zamykam plik

    def loadListOfPages(self, fileName): #ładuje liste z wybranego pliku. Każda strona musi się znajdować w odpowiedniej linii
        try:
            with open(fileName) as file:
                listOfLines = file.read().splitlines() #dzieli stringa na liste gdzie każda linia to jej element
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        for i in range(0, len(listOfLines)):
            self.listOfPages[i] = listOfLines[i] #zapisuje strone ze stworzonej wczesniej listy linii z pliku
        file.close()
