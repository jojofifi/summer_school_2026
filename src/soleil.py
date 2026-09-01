import pygame
import drawmethod
import math


class Soleil():
    def __init__(self,display,x,y,time):
        self.x = x
        self.y = y
        self.time = time
        self.display = display
        self.angle = 22.2
        self.distance = 450
        self.acceleration = 2*self.distance/math.pow(self.time,2)
        self.initial_speed = self.acceleration * (self.time/2) / math.sin(math.radians(self.angle))
        self.gravity = 2*self.distance/math.pow(self.time,2)
        self.end = False
        self.timer = 0
        self.rayon = 30
        self.nbr_point = 10
        self.color = (255, 215, 0)
    def move(self):
        if not self.end:
            self.speedx = self.initial_speed*math.cos(math.radians(self.angle))
            self.speedy = (self.gravity)*self.timer+self.initial_speed*-math.sin(math.radians(self.angle))
            self.x += self.speedx*1/90
            self.y += self.speedy*1/90
            self.timer += 1/90
        if self.timer >= self.time/4:
            self.end = True
    def draw(self):
        drawmethod.drawcircle(self.display,self.color,self.x,self.y,self.rayon,self.nbr_point)
        drawmethod.draw_rays(self.display,self.color,self.x,self.y,self.rayon,self.nbr_point)
    

        
        