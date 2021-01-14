from generator import generateListOfPages


class symulation:  # symuluje algorytmy, czyści plik i zapisuje wyniki do niego tworzy też jakby troche maina (main process)
    def __init__(self, numberOfPages, frameSize, pagesRange,
                 load):  # tworząc klase mozemy wybrac ilosc stron wielkosc ramki rozmiar do jakiego numeru ma byc ramka i czy mamy wczytywać z pliku
        self.frameSize = frameSize
        self.numberOfPages = numberOfPages
        self.pagesRange = pagesRange
        self.generateList = generateListOfPages(self.numberOfPages,
                                                self.pagesRange)  # tworze klase generate List z generator py
        if load:  # jezeli chce dane z pliku
            self.generateList.loadListOfPages("load.txt")
        self.listOfPages = self.generateList.listOfPages
        self.frameList = []
        self.timeInFrame = []
        self.appealCounter = []
        self.time = 0
        for i in range(0,
                       self.generateList.pagesRange + 1):  # generuje listy do algorytmow która będzie miała wielkość taką jak najwieksza mozliwa liczba ramki
            self.timeInFrame.append(-1)  # wypełniam ja nieralną małą liczbą bym potem mogł w lru dobrze porównywać
            self.appealCounter.append(1000)  # wypełniam nieralną dużą liczbą bym potem mogł w lfu dobrze porównywać
        self.nextFrame = 0
        self.clearFile()  # czyszcze plik
        self.replacements = 0
        self.hits = 0

    def LRU(self):
        self.replacements = self.replacements + 1
        foundMatch = 0  # zeruje znaleziony wynik
        oldest = -10000  # do porównywania
        for i in range(0, len(self.timeInFrame)):  # znajduje najwiekszy czas
            if self.timeInFrame[i] >= oldest:  # szukam  czasu najstarszej ramki i przypisuje do zmiennej oldest
                oldest = self.timeInFrame[i]
        for i in range(0, len(self.timeInFrame)):  # szukam dla którego numeru i w liscie z czasem mamy taki sam oldest
            if oldest == self.timeInFrame[i]:
                foundMatch = i  # przypisuje numer listy dla którego czas najstarszej ramki jest równy elementowi w liscie
                self.timeInFrame[i] = -1  # wyrzucam ten numer z ramki wiec zatrzumuje jego licznik czasu
        for i in range(0, len(self.frameList)):
            if int(self.frameList[
                       i]) == foundMatch:  # szukam dla ktorego numeru listy w ramce znalezione dopasowanie bedzie takie samo
                self.nextFrame = i  # zapisuje numer nastepnej ramki

    def symLRU(
            self):  # symuluje LRU tzn robie operacje na listach i zarządzam ramkami tzn tworze im logike.. czy maja byc zmienione czy nie itp
        for element in range(0, len(self.listOfPages)):  # szuma po calej liscie stron
            self.saveData(element)  # zapisuje Liste do pliku za kazdym razem by łatwiej śledzić wyniki
            for i in range(0, len(self.timeInFrame)):  # zwiekszam czas jezeli wykorzystany
                if self.timeInFrame[i] != -1:
                    self.timeInFrame[i] = self.timeInFrame[i] + 1
            if int(self.listOfPages[element]) in self.frameList:  # jezeli strona w ramce
                self.hits = self.hits + 1  # zwiekszam hit
                self.timeInFrame[int(self.listOfPages[element])] = 0  # zeruje czas dla tej strony
            elif len(self.frameList) < self.frameSize:  # jezeli jest miejsce w ramce
                self.timeInFrame[int(self.listOfPages[element])] = 0  # wlaczam czas dla strony
                self.frameList.append(int(self.listOfPages[element]))  # dodaje element do ramki
            else:  # jezeli strony nie ma w ramce a ramka jest pelna
                self.LRU()
                self.frameList[self.nextFrame] = int(self.listOfPages[
                                                         element])  # podmieniam odpowiednią strone w ramce na nową strone wedlug algorytmu LRU
                self.timeInFrame[int(self.listOfPages[element])] = 0  # zeruje czas dla nowej strony w ramce

    def LFU(self):
        self.replacements = self.replacements + 1
        smallest = 10000
        foundedMatch = []
        theOne = 0
        choosen = False
        for i in range(0, len(self.frameList)):  # szukam najmniejszej ilsoci odwołań do strony sposród stron z ramki
            if self.appealCounter[self.frameList[i]] < smallest:
                smallest = self.appealCounter[
                    self.frameList[i]]  # zapisuje najmniejsza liczbe odwołań jaką udało mi sie znaleźć
        for i in range(0, len(self.frameList)):
            if smallest == self.appealCounter[self.frameList[
                i]]:  # jezeli najmniejsza liczba jaka znalazlem jest taka sama dla paru odniesien w liscie to tworze liste dopasowanych stron
                foundedMatch.append(self.frameList[i])
        for i in range(0, len(
                self.listOfPages)):  # robie tu kolejke ze jeżeli ilosc wystąpień taka sama to weź według fifo
            for j in range(0, len(foundedMatch)):
                if foundedMatch[j] == int(self.listOfPages[i]):
                    theOne = foundedMatch[j]
                    choosen = True
                    break
            if choosen:
                break
        for i in range(0, len(self.frameList)):  # szukam numeru z ramki do zastąpienia
            if int(self.frameList[i]) == theOne:
                self.nextFrame = i

    def symLFU(
            self):  # symuluje LRU tzn robie operacje na listach i zarządzam ramkami tzn tworze im logike.. czy maja byc zmienione czy nie itp
        for element in range(0, len(self.listOfPages)):
            self.saveData(element)
            if int(self.listOfPages[
                       element]) in self.frameList:  # jezeli strona jest w ramce to zwiekszam jej ilosc wystapien i trafienia
                self.hits = self.hits + 1
                self.appealCounter[int(self.listOfPages[element])] = self.appealCounter[
                                                                         int(self.listOfPages[element])] + 1
            elif len(
                    self.frameList) < self.frameSize:  # jezeli jest miejsce w ramce to wlaczam licznik wystapien i dodaje 1
                self.appealCounter[int(self.listOfPages[element])] = 0
                self.appealCounter[int(self.listOfPages[element])] = self.appealCounter[
                                                                         int(self.listOfPages[element])] + 1
                self.frameList.append(int(self.listOfPages[element]))  # dodaje strone do ramki
            else:  # jezeli nie ma w ramce i ramka pelna
                self.LFU()  # wybieram element do zastąpienia
                self.frameList[self.nextFrame] = int(self.listOfPages[element])
                if self.appealCounter[int(self.listOfPages[
                                              element])] == 1000:  # jezeli jest to nowy element to go zeruje tzn wlaczam do liczenia
                    self.appealCounter[int(self.listOfPages[element])] = 0
                self.appealCounter[int(self.listOfPages[element])] = self.appealCounter[
                                                                         int(self.listOfPages[element])] + 1

    def mainProcess(self,
                    algorithmName):  # cos w stylu maina, odpowiada za wybranie odpowiedniego algorytmu i zapis do pliku oraz wypisania wyników w terminale
        try:
            self.file = open("Outcome.txt", 'a')
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        if algorithmName == "LRU":
            print(algorithmName)
            self.file.write(algorithmName)
            self.file.write("\n")
            self.symLRU()
            self.saveData(len(self.listOfPages))
        elif algorithmName == "LFU":
            print(algorithmName)
            self.file.write("\n")
            self.file.write(algorithmName)
            self.file.write("\n")
            self.symLFU()
        self.saveData(len(self.listOfPages))
        self.printOutcome()
        self.saveOutcome()
        self.hits = 0
        self.replacements = 0
        self.clearFrame()
        self.file.close()

    def saveData(self, element):  # funkcja pozwalajaca mała ilością kodu zapisać wszystko do pliku
        self.file.write("krok ")
        self.file.write(str(element))
        self.file.write(" ")
        self.file.writelines(str(self.listOfPages))
        self.file.write("\n")
        self.file.writelines(str(self.frameList))
        self.file.write("\n")

    def saveOutcome(self):
        self.file.write("replacements: ")
        self.file.write(str(self.replacements))
        self.file.write("\n")
        self.file.write("hits: ")
        self.file.write(str(self.hits))

    def printOutcome(self):
        print(self.listOfPages)
        print(self.frameList)
        print("zastapienia", self.replacements)
        print("trafienia:", self.hits)

    def clearFile(self):
        try:
            self.file = open("Outcome.txt", 'w')
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        self.file.close()

    def clearFrame(self):
        self.frameList = []


sym = symulation(15, 3, 7, True)
sym.mainProcess("LRU")
sym.mainProcess("LFU")
