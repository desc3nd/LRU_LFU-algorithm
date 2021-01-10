from generator import generateListOfPages


class symulation:
    def __init__(self, numberOfPages, frameSize, pagesRange):
        self.frameSize = frameSize
        self.numberOfPages = numberOfPages
        self.pagesRange = pagesRange
        self.generateList = generateListOfPages(self.numberOfPages, self.pagesRange)
        self.listOfPages = self.generateList.listOfPages
        self.frameList = []
        self.timeInFrame = []
        self.appealCounter = []
        self.time = 0
        for i in range(0, self.generateList.pagesRange + 1):
            self.timeInFrame.append(-1)
            self.appealCounter.append(1000)
        self.nextFrame = 0

    def LRU(self):
        foundedMatch = 0
        oldest = -1000
        for i in range(1, len(self.timeInFrame)):
            if self.timeInFrame[i] > oldest:
                oldest = self.timeInFrame[i]
        for i in range(0, len(self.timeInFrame)):
            if oldest == self.timeInFrame[i]:
                foundedMatch = i
        self.timeInFrame[foundedMatch] = 0
        for i in range(0, len(self.frameList)):
            if self.frameList[i] == foundedMatch:
                self.nextFrame = i

    def LFU(self):
        smallest = 1000
        foundedMatch = 0
        for i in range(1, len(self.appealCounter)):
            if self.appealCounter[i] < smallest:
                smallest = self.appealCounter[i]
        for i in range(0, len(self.appealCounter)):
            if smallest == self.appealCounter[i]:
                foundedMatch = i
        self.timeInFrame[foundedMatch] = 0
        for i in range(0, len(self.frameList)):
            if self.frameList[i] == foundedMatch:
                self.nextFrame = i

    def mainProcess(self, algorithmName):
        try:
            self.file = open("Outcome.txt", 'w')
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        if algorithmName == "LRU":
            self.file.write("LRU")
            self.file.write("\n")
            for element in range(0, len(self.listOfPages)):
                self.saveData(element)
                for i in range(0, len(self.timeInFrame)):
                    if self.timeInFrame[i] != -1:
                        self.timeInFrame[i] = self.timeInFrame[i] + 1
                if self.listOfPages[element] in self.frameList:
                    self.timeInFrame[self.listOfPages[element]] = 0
                elif len(self.frameList) < self.frameSize:
                    self.timeInFrame[self.listOfPages[element]] = 0
                    self.frameList.append(self.listOfPages[element])
                else:
                    self.LRU()
                    self.frameList[self.nextFrame] = self.listOfPages[element]
        elif algorithmName == "LFU":
            self.file.write("LFU")
            self.file.write("\n")
            for element in range(0, len(self.listOfPages)):
                self.saveData(element)
                if self.listOfPages[element] in self.frameList:
                    self.appealCounter[self.listOfPages[element]] = self.appealCounter[self.listOfPages[element]] + 1
                elif len(self.frameList) < self.frameSize:
                    self.appealCounter[self.listOfPages[element]] = 0
                    self.appealCounter[self.listOfPages[element]] = self.appealCounter[self.listOfPages[element]] + 1
                    self.frameList.append(self.listOfPages[element])
                else:
                    self.LFU()
                    self.frameList[self.nextFrame] = self.listOfPages[element]
        print(self.listOfPages)
        print(self.frameList)
        self.file.close()

    def saveData(self, element):
        self.file.write("krok ")
        self.file.write(str(element))
        self.file.write(" ")
        self.file.writelines(str(self.listOfPages))
        self.file.write("\n")
        self.file.writelines(str(self.frameList))
        self.file.write("\n")



sym = symulation(10, 4, 10)
sym.mainProcess("LFU")
sym.mainProcess("LRU")