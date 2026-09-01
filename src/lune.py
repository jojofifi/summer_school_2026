import pygame
import drawmethod
import math


class Lune():
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
        self.rayon = 40
    def move(self):
        self.speedx = self.initial_speed*math.cos(math.radians(self.angle))
        self.speedy = (self.gravity)*self.timer+self.initial_speed*-math.sin(math.radians(self.angle))
        self.x += self.speedx*1/90
        self.y += self.speedy*1/90
        self.timer += 1/90
        if self.timer >= self.time:
            self.end = True
            self.x = 1050
            self.y = 200

    def draw(self,color2):
        drawmethod.drawcircle(self.display,(142,142,142),self.x,self.y,self.rayon,15)
        drawmethod.drawcircle(self.display,color2,self.x-30,self.y,self.rayon,15)
        