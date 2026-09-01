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
                if arrNoise[i][j] < 0.45:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "mountain", self.screen))
                elif arrNoise[i][j] < 0.55:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "plains", self.screen))
                else:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "water", self.screen))
        return tiles




class Tile:
    def __init__(self, coordinateStart:tuple[float,float], coordinateEnd:tuple[float,float], typeName:str, screen:pygame.Surface):
        self.type = typeName
        self.coordinateStart = coordinateStart
        self.coordinateEnd = coordinateEnd
        self.screen = screen
        baseLength = math.ceil(self.coordinateEnd[0] - self.coordinateStart[0])
        self.mountain = Mountain(4, 20, 10, baseLength - 10, math.ceil(baseLength / 6), 20, 25, self.coordinateStart,self.screen)





    def drawType(self):
        width = self.coordinateEnd[0] - self.coordinateStart[0]
        middleHigh = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] - (width / 4))
        middleLow = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] + (width / 4))
        if self.type == "mountain":
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
            self.mountain.drawMountain()
        elif self.type == "plains":
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
        elif self.type == "water":
            pygame.draw.polygon(self.screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(self.screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleLow))