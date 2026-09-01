# Example file showing a basic pygame "game loop"
import pygame
import math
import random
import numpy as np

class Mountain:
    def __init__(self, nbrLevels: int, nextLvlSizeReduce: int, points: int, baseLength: int, height: int, sizeDiff: int, lowPerc: int, startCoordinates: tuple[float, float], screen: pygame.Surface):
        self.nbrLevels = nbrLevels
        self.nextLvlSizeReduce = nextLvlSizeReduce
        self.points = points
        self.baseLength = baseLength
        self.height = height
        self.sizeDiff = sizeDiff
        self.lowPerc = lowPerc
        self.startCoordinates = startCoordinates
        self.screen = screen
        self.levels = []
        Mountain.createMountain(self)

    def lineCreate(self, points:int, length:int, startCoordinates:tuple[float, float], lowPer:int):
        steps = math.ceil(math.ceil(points / 2) / 2)
        arr = []
        nextX = []
        nextY = np.zeros(points, dtype=int)

        xCalc = length/(points-1)
        for i in range(0, points):
            if i == 0:
                nextX.append(startCoordinates[0])
            elif i == points -1:
                nextX.append(startCoordinates[0]+length)
            else:
                rdm = random.randint(math.ceil(xCalc * i - xCalc / 2) * 100, math.ceil(xCalc * i + xCalc / 2) * 100) / 100
                nextX.append(startCoordinates[0]+rdm)

        for i in range(0, math.ceil(points/2)):
            # starting point
            if i == 0:
                nextY[i] = startCoordinates[1]
                nextY[points - i - 1] = startCoordinates[1]
            elif i == 1:
                nextY[i] = nextY[i - 1] + (length * ((lowPer/steps) / 100))
                nextY[points - i-1] = nextY[i - 2] + (length * ((lowPer/steps) / 100))

            elif i % 2 == 1:
                nextY[i] = nextY[i - 2] + (length * ((lowPer/steps) / 100))
                nextY[points - i - 1] = nextY[i - 2] + (length * ((lowPer/steps) / 100))
            elif i % 2 == 0:
                nextY[i] = random.randint(math.ceil(nextY[i - 2] * 10), math.ceil(nextY[i - 1] * 10)) / 10
                nextY[points - i-1] = random.randint(math.ceil(nextY[points - i-1 + 2] * 10), math.ceil(nextY[points - i-1 + 1] * 10)) / 10
            else:
                nextY[i] = startCoordinates[1] + (length * (lowPer / 100))
                nextY[points - i - 1] = startCoordinates[1] + (length * (lowPer / 100))

        for i in range(0, len(nextX)):
            arr.append([nextX[i], float(nextY[i])])

        return arr

    def levelCreate(self, points:int, baseLength:int, height:int, sizeDiff:int, lowPerc:int, startCoordinates:tuple[float, float]):
        bottomCoords = Mountain.lineCreate(self, points,baseLength,startCoordinates,lowPerc)
        topStartCoord = (startCoordinates[0]+(baseLength*sizeDiff/2/100),startCoordinates[1]-height)
        topCoords = Mountain.lineCreate(self, points,int(baseLength-(baseLength*(sizeDiff/100))),topStartCoord,lowPerc)
        return bottomCoords, topCoords

    def drawLevel(self, arrLow:list, arrHigh:list):
        for i in range(0, len(arrHigh)-1):
            if i % 2 == 0:
                newRGB = random.randint(0,100)
                colorBackground = (37, newRGB, newRGB)
            else:
                newRGB = random.randint(100, 200)
                colorBackground = (37, newRGB, newRGB)
            pygame.draw.polygon(self.screen, colorBackground, (arrLow[i], arrHigh[i], arrHigh[i+1]))
            pygame.draw.polygon(self.screen, colorBackground, (arrLow[i], arrLow[i+1], arrHigh[i+1]))
            if i < len(arrHigh)-2:
                colorBackground = (244, 233, 201)
                pygame.draw.polygon(self.screen, colorBackground, (arrHigh[0], arrHigh[i+1], arrHigh[i+2]))
        colorBackground = (0, 255, 0)
        diff = arrHigh[math.ceil(len(arrHigh)/2)][1] - arrHigh[0][1]
        pointYHigh = arrHigh[math.ceil(len(arrHigh)/2)][0], arrHigh[math.ceil(len(arrHigh)/2)][1]-diff*3
        pygame.draw.polygon(self.screen, colorBackground, (arrHigh[0], pointYHigh, arrHigh[len(arrHigh)-1]))


    def createMountain(self):
        self.levels.append(Mountain.levelCreate(self, self.points, self.baseLength, self.height, self.sizeDiff, self.lowPerc, self.startCoordinates))

        for i in range(0, self.nbrLevels-1):
            newLength = self.levels[i][1][len(self.levels[i][1])-1][0]-self.levels[i][1][0][0]
            newLength = newLength - newLength * self.nextLvlSizeReduce / 100
            newCoords = self.levels[i][1][0][0] + newLength * self.nextLvlSizeReduce / 2 / 100, self.levels[i][1][0][1]

            if i == self.nbrLevels -2:
                self.levels.append(Mountain.levelCreate(self, 3, newLength, int(self.height/1.2), self.sizeDiff + 40, self.lowPerc-8, newCoords))
            else:
                self.levels.append(Mountain.levelCreate(self, self.points, newLength, int(self.height + self.height * 0.2), self.sizeDiff + 15, self.lowPerc, newCoords))

    def drawMountain(self):
        for level in self.levels:
            Mountain.drawLevel(self, level[0], level[1])
