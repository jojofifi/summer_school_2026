import sys
import pygame
import math
from mountain import Mountain
from opensimplex import OpenSimplex
import numpy as np

class Tiles:
    def __init__(self, start:tuple[float,float], screen:pygame.Surface, height:float, width:float, tileWidth:float) -> None:
        self.type = type
        self.start = start
        self.screen = screen
        self.height = height
        self.width = width
        self.tileWidth = tileWidth

    def createTiles(self, seed, zoom):
        tmp = OpenSimplex(seed=seed)
        line = math.ceil(self.height/(self.tileWidth/2)+1)
        column = math.ceil(self.width/ self.tileWidth)+1
        arrNoise = np.zeros((line, column))
        tiles = []

        for i in range(0,line):
            for j in range(0, column):
                nx = i / zoom
                ny = j / zoom
                value = tmp.noise2(nx, ny)
                arrNoise[i][j] = (value + 1.0) / 2.0

                if(i%2 == 0):
                    coordinateStart = (self.start[0] + j*self.tileWidth, (self.start[1]+i*self.tileWidth/4)+i)
                else:
                    coordinateStart = (self.start[0] + (j * self.tileWidth) - (self.tileWidth / 2),(self.start[1] + i * self.tileWidth / 4) + i)
                coordinateEnd = (coordinateStart[0] + self.tileWidth, coordinateStart[1])
                if arrNoise[i][j] < 0.35:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "mountainTall", self.screen, arrNoise[i][j]))
                elif arrNoise[i][j] < 0.45:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "mountainSmall", self.screen, arrNoise[i][j]))
                elif arrNoise[i][j] < 0.55:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "plains", self.screen, arrNoise[i][j]))
                else:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "water", self.screen, arrNoise[i][j]))
        return tiles




class Tile:
    def __init__(self, coordinateStart:tuple[float,float], coordinateEnd:tuple[float,float], typeName:str, screen:pygame.Surface, noise:float):
        self.type = typeName
        self.coordinateStart = coordinateStart
        self.coordinateEnd = coordinateEnd
        self.screen = screen

        mountainCoords = ((coordinateStart[0] + (coordinateEnd[0] - coordinateStart[0]) * 0.1),coordinateStart[1])
        baseLength = math.ceil((coordinateEnd[0] - coordinateStart[0])*0.8)
        if self.type == "mountainTall":
            self.mountain = Mountain(4, 20, 10, baseLength, math.ceil((baseLength / 6)+(baseLength / 6)*noise), 20, 25, mountainCoords,self.screen)
        elif self.type == "mountainSmall":
            self.mountain = Mountain(3, 20, 10, baseLength, math.ceil((baseLength / 6)+(baseLength / 6)*noise), 20, 25, mountainCoords,self.screen)

    def drawType(self):
        width = self.coordinateEnd[0] - self.coordinateStart[0]
        middleHigh = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] - (width / 4))
        middleLow = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] + (width / 4))
        if self.type == "plains":
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
        elif self.type == "water":
            pygame.draw.polygon(self.screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleLow))
        else:
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
            self.mountain.drawMountain()