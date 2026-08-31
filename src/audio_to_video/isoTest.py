import sys
import pygame
import math
from mountain import Mountain

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

    def fillBottomScreen(self):
        tiles = []
        for i in range(0,math.ceil(SCREEN_HEIGHT/(TILE_WIDTH/4))):
            for j in range(0, math.ceil(SCREEN_WIDTH/ TILE_WIDTH)):
                if(i%2 == 0):
                    coordinateStart = (self.start[0] + j*TILE_WIDTH, (self.start[1]+i*TILE_WIDTH/4)+i)
                else:
                    coordinateStart = (self.start[0] + (j * TILE_WIDTH) - (TILE_WIDTH / 2),(self.start[1] + i * TILE_WIDTH / 4) + i)
                coordinateEnd = (coordinateStart[0] + TILE_WIDTH, coordinateStart[1])
                tiles.append(Tile(coordinateStart, coordinateEnd, "mountain",self.screen))
        return tiles




class Tile:
    def __init__(self, coordinateStart:tuple[float,float], coordinateEnd:tuple[float,float], typeName:str, screen:pygame.Surface):
        self.type = typeName
        self.coordinateStart = coordinateStart
        self.coordinateEnd = coordinateEnd
        self.screen = screen

        width = coordinateEnd[0] - coordinateStart[0]
        middleHigh = ((coordinateStart[0] + width / 2), coordinateStart[1] - (width / 4))
        middleLow = ((coordinateStart[0] + width / 2), coordinateStart[1] + (width / 4))
        pygame.draw.polygon(screen, (59, 153, 0), (coordinateStart, coordinateEnd, middleHigh))
        pygame.draw.polygon(screen, (59, 153, 0), (coordinateStart, coordinateEnd, middleLow))

    def drawType(self):
        if self.type == "mountain":
            baseLength = math.ceil(self.coordinateEnd[0] - self.coordinateStart[0])
            print(baseLength)
            #todo pass arguments in self for mountains
            mountain = Mountain(3,20,10, baseLength-10, 100, 20, 25, self.coordinateStart, self.screen)
            mountain.drawMountain(3,20,10, baseLength-10, 15, 20, 25, self.coordinateStart)



tiles1 = Tiles(START_COORDINATES, screen)
tiles = tiles1.fillBottomScreen()
for i in range(0,len(tiles)-1):
    tiles[i].drawType()

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