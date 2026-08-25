from feux1 import Firework
from feux1 import Explosion
import pygame
import random

pygame.init()

screen_height = 600
screen_width = 1000
display = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
FPS = 90

fireworks = []
explosions = []
run = True
while run:

    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

    display.fill((0, 0, 0))
    if random.uniform(1,100) <=6:
        fireworks.append(Firework(random.randint(2,10),display,random.randint(1,127),10))


    for firework in fireworks:
        firework.move()
        firework.draw()
        if firework.end:
            for i in range(random.randint(20,40)):
                 explosions.append(Explosion(display,firework.x,firework.y,firework.color,random.randint(90,180)))
            fireworks.remove(firework)
            del firework
    for explosion in explosions:
        explosion.move()
        explosion.draw()
        if explosion.end:
            explosions.remove(explosion)
            del explosion
            

    pygame.display.update()
    clock.tick(FPS)
pygame.quit