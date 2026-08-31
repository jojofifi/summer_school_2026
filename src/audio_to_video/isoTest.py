import sys
import pygame
import math
from mountain import Mountain
from opensimplex import OpenSimplex
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_WIDTH = 140
START_COORDINATES = (0,SCREEN_HEIGHT/2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class Tiles:
    def __init__(self, start:tuple[float,float], screen:pygame.Surface) -> None:
        self.type = type
        self.start = start
        self.screen = screen

    def fillBottomScreen(self, seed, zoom):
        tmp = OpenSimplex(seed=seed)

        line = math.ceil(SCREEN_HEIGHT/(TILE_WIDTH/2)+1)
        print(line)
        column = math.ceil(SCREEN_WIDTH/ TILE_WIDTH)+1
        arrNoise = np.zeros((line, column))
        tiles = []
        for i in range(0,line):
            for j in range(0, column):
                nx = i / zoom
                ny = j / zoom
                value = tmp.noise2(nx, ny)
                arrNoise[i][j] = (value + 1.0) / 2.0

                if(i%2 == 0):
                    coordinateStart = (self.start[0] + j*TILE_WIDTH, (self.start[1]+i*TILE_WIDTH/4)+i)
                else:
                    coordinateStart = (self.start[0] + (j * TILE_WIDTH) - (TILE_WIDTH / 2),(self.start[1] + i * TILE_WIDTH / 4) + i)
                coordinateEnd = (coordinateStart[0] + TILE_WIDTH, coordinateStart[1])
                if arrNoise[i][j] < 0.45:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "mountain", self.screen))
                elif arrNoise[i][j] < 0.55:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "plains", self.screen))
                else:
                    tiles.append(Tile(coordinateStart, coordinateEnd, "water", self.screen))
        print(arrNoise)
        return tiles




class Tile:
    def __init__(self, coordinateStart:tuple[float,float], coordinateEnd:tuple[float,float], typeName:str, screen:pygame.Surface):
        self.type = typeName
        self.coordinateStart = coordinateStart
        self.coordinateEnd = coordinateEnd
        self.screen = screen
        Tile.drawType(self)



    def drawType(self):
        width = self.coordinateEnd[0] - self.coordinateStart[0]
        middleHigh = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] - (width / 4))
        middleLow = ((self.coordinateStart[0] + width / 2), self.coordinateStart[1] + (width / 4))
        if self.type == "mountain":
            pygame.draw.polygon(screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
            baseLength = math.ceil(self.coordinateEnd[0] - self.coordinateStart[0])
            mountain = Mountain(4,20,10, baseLength-10, math.ceil(baseLength/6), 20, 25, self.coordinateStart, self.screen)
            mountain.drawMountain()
        elif self.type == "plains":
            pygame.draw.polygon(screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(screen, (59, 153, 0), (self.coordinateStart, self.coordinateEnd, middleLow))
        elif self.type == "water":
            pygame.draw.polygon(screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleHigh))
            pygame.draw.polygon(screen, (70, 189, 240), (self.coordinateStart, self.coordinateEnd, middleLow))



tiles1 = Tiles(START_COORDINATES, screen)
tiles = tiles1.fillBottomScreen(1,2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    #updates the screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()