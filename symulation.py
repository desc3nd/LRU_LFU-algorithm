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
                # print("lala")
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
        if algorithmName == "LRU":
            for element in range(0, len(self.listOfPages)):
                for i in range(0, len(self.timeInFrame)):
                    if self.timeInFrame[i] != -1:
                        self.timeInFrame[i] = self.timeInFrame[i] + 1
                if self.listOfPages[element] in self.frameList:
                    self.timeInFrame[self.listOfPages[element]] = 0
                elif len(self.frameList) < self.frameSize:
                    self.timeInFrame[self.listOfPages[element]] = 0
                    self.frameList.append(self.listOfPages[element])
                else:
                    print('wch')
                    self.LRU()
                    self.frameList[self.nextFrame] = self.listOfPages[element]
        elif algorithmName == "LFU":
            for element in range(0, len(self.listOfPages)):
                print("krok", element)
                print(self.listOfPages)
                print(self.frameList)
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

    def saveData(self, fileName):
        try:
            file = open(fileName, 'w')
        except Exception as exc:
            print("Nie mozna otworzyc pliku:", exc)
        for i in range(0, self.numberOfPages):
            file.write("krok: ")
            file.write(str(i))
            file.write('\n')
            for i in self.listOfPages:
                file.write(str(i))
                file.write(" ")
            file.write("\n")
            for i in self.frameList:
                file.write(str(i))
                file.write(" ")
            file.write('\n')
        try:
            file.close()
        except Exception as exc:
            print("Nie mozna zamknac pliku:", exc)




sym = symulation(10, 4, 10)
sym.mainProcess("LFU")
sym.saveData("correctPages.txt")
