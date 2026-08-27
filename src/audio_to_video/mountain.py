# Example file showing a basic pygame "game loop"
import pygame
import math
import random
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


def lineCreate(faces:int, length:int, startCoordinates:tuple[float, float], lowPer:int):
    steps = math.ceil(math.ceil(faces / 2) / 2)
    arr = []
    nextX = []
    nextY = np.zeros(faces, dtype=int)

    xCalc = length/faces
    for i in range(0, faces):
        if i == 0:
            nextX.append(startCoordinates[0])
        elif i == faces -1:
            nextX.append(startCoordinates[0]+length)
        else:
            rdm = random.randint(math.ceil(xCalc * i - xCalc / 2) * 100, math.ceil(xCalc * i + xCalc / 2) * 100) / 100
            nextX.append(startCoordinates[0]+rdm)

    for i in range(0, math.ceil(faces/2)):
        # starting point
        if i == 0:
            nextY[i] = startCoordinates[1]
            nextY[faces - i - 1] = startCoordinates[1]
        elif i == 1:
            nextY[i] = nextY[i - 1] + (length * ((lowPer/steps) / 100))
            nextY[faces - i-1] = nextY[i - 2] + (length * ((lowPer/steps) / 100))

        elif i % 2 == 1:
            nextY[i] = nextY[i - 2] + (length * ((lowPer/steps) / 100))
            nextY[faces - i - 1] = nextY[i - 2] + (length * ((lowPer/steps) / 100))
        elif i % 2 == 0:
            nextY[i] = random.randint(math.ceil(nextY[i - 2] * 10), math.ceil(nextY[i - 1] * 10)) / 10
            nextY[faces - i-1] = random.randint(math.ceil(nextY[faces - i-1 + 2] * 10), math.ceil(nextY[faces - i-1 + 1] * 10)) / 10
        else:
            nextY[i] = startCoordinates[1] + (length * (lowPer / 100))
            nextY[faces - i - 1] = startCoordinates[1] + (length * (lowPer / 100))

    for i in range(0, len(nextX)):
        arr.append([nextX[i], float(nextY[i])])

    return arr

def levelCreate(faces:int, baseLength:int, height:int, sizeDiff:int, lowPerc:int, startCoordinates:tuple[float, float]):
    bottomCoords = lineCreate(faces,baseLength,startCoordinates,lowPerc)
    topStartCoord = (startCoordinates[0]+(baseLength*sizeDiff/2/100),startCoordinates[1]-height)
    topCoords = lineCreate(faces,int(baseLength-(baseLength*(sizeDiff/100))),topStartCoord,lowPerc)
    return bottomCoords, topCoords

def drawLevel(arrLow:list, arrHigh:list):
    colorBackground = (0, 255, 0)
    print(arrLow)
    print(arrHigh)
    for i in range(0, len(arrHigh)-1):
        if i % 2 == 0:
            colorBackground = (0, 0, 255)
        else:
            colorBackground = (255, 0, 0)
        pygame.draw.polygon(screen, colorBackground, (arrLow[i], arrHigh[i], arrHigh[i+1]))
        pygame.draw.polygon(screen, colorBackground, (arrLow[i], arrLow[i+1], arrHigh[i+1]))
        if i < len(arrHigh)-2:
            colorBackground = (0, 255, 0)
            pygame.draw.polygon(screen, colorBackground, (arrHigh[0], arrHigh[i+1], arrHigh[i+2]))
    colorBackground = (0, 255, 0)
    diff = arrHigh[math.ceil(len(arrHigh)/2)][1] - arrHigh[0][1]
    pointYHigh = arrHigh[math.ceil(len(arrHigh)/2)][0], arrHigh[math.ceil(len(arrHigh)/2)][1]-diff*3
    print(pointYHigh)
    pygame.draw.polygon(screen, colorBackground, (arrHigh[0], pointYHigh, arrHigh[len(arrHigh)-1]))


def drawMountain(nbrLevels: int, nextLvlSizeReduce: int, points: int, baseLength: int, height: int, sizeDiff: int, lowPerc: int, startCoordinates: tuple[float, float]):
    level = levelCreate(points, baseLength, height, sizeDiff, lowPerc, startCoordinates)
    drawLevel(level[0], level[1])

    for i in range(1, nbrLevels):
        newLength = level[1][len(level[1])-1][0]-level[1][0][0]
        print(newLength)
        newLength = newLength - newLength * nextLvlSizeReduce / 100
        print(newLength)
        print()
        newCoords = level[1][0][0] + newLength * nextLvlSizeReduce / 2 / 100, level[1][0][1]

        if i == nbrLevels -1:
            level = levelCreate(3, newLength, int(height/1.2), sizeDiff + 40, lowPerc-8, newCoords)
        else:
            level = levelCreate(points, newLength, int(height + height * 0.2), sizeDiff + 15, lowPerc, newCoords)

        drawLevel(level[0], level[1])



drawMountain(3,20,10, 300, 100, 20, 15, (1280 / 2, 720 / 2))
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()