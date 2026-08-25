import random
import pygame
import math

Color = {
    0 : (255,0,0),     # rouge
    1 : (255,128,0),   # orange
    2 : (255,255,0),   # jaune
    3 : (128,255,0),   # vert clair
    4 : (0,255,0),     # vert
    5 : (0,255,255),   # bleu cyan
    6 : (0,128,255),   # bleu 
    7 : (0,0,255),     # bleu foncée
    8 : (127,0,255),   # violet
    9 : (255,0,255),   # rose
    10 : (255,0,127),  # magenta
    11 : (178,102,255),# mauve
}

def get_note_from_pitch(pitch):
    valeur = pitch%12
    return Color[int(valeur)]

class Firework():
    def __init__(self,time,display,pitch,ended_explosion):
        self.x = random.uniform(0,1000)
        self.y = 500
        self.distance = 450
        self.time = time
        self.acceleration = 2*self.distance/math.pow(self.time,2)
        self.initial_speed = self.acceleration*self.time
        self.end = False
        self.display = display
        self.timer = 0
        self.color = get_note_from_pitch(pitch)
        
    def move(self):
        self.timer += 1/90
        self.speed = self.initial_speed-self.acceleration*self.timer
        self.y -= self.speed * 1/90
        if self.speed <= 0:
            self.end = True
    def draw(self):
        a = [self.x,self.y-10]
        b = [self.x-10,self.y+10]
        c = [self.x+10,self.y+10]
        pygame.draw.polygon(self.display,self.color,(a,b,c))

class Explosion():
    def __init__(self,display,x,y,color,ended_explosion):
        self.x = x
        self.y = y
        self.angle = random.uniform(0,360)
        self.vx = math.cos(math.radians(self.angle))
        self.vy = -math.sin (math.radians(self.angle))
        self.color = color
        self.end_time = ended_explosion
        self.timer = 0
        self.end = False
        self.display = display
        self.trails = []

    def move(self):
        if self.y < 550 :
            self.vy += 0.01
        self.trails.insert(0,Trail(self.x,self.y,self.timer,self.color,self.display))
        if(len(self.trails) > 50):
            del self.trails[len(self.trails) - 1]

        for trail in self.trails:
            trail.update()

        self.timer += 1
        self.x += self.vx
        self.y += self.vy
        if self.timer == 90:
            self.end = True
    def draw(self):
        a = [self.x,self.y-10]
        b = [self.x-10,self.y+10]
        c = [self.x+10,self.y+10]
        drawcircle(self.display,self.color,self.x,self.y,5,10)

class Trail():
    def __init__(self,x,y,timer,color,display):
        self.x = x
        self.y = y 
        self.timer = timer
        self.color = color
        self.display = display
        self.a = [self.x,self.y-3]
        self.b = [self.x-3,self.y+3]
        self.c = [self.x+3,self.y+3]
        pygame.draw.polygon(self.display,self.color,(self.a,self.b,self.c))
    def update(self):
        pygame.draw.polygon(self.display,(0,0,0),(self.a,self.b,self.c))
        self.a = [self.x,self.a[1]+0.01]
        self.b = [self.b[0]+0.01,self.b[1]-0.01]
        self.c = [self.c[0]-0.01,self.c[1]-0.01]
        pygame.draw.polygon(self.display,self.color,(self.a,self.b,self.c))
def drawcircle(display,color,x,y,rayon,nbr_point):
    angle = 360/nbr_point
    new_angle = 0
    center = [int(x),int(y)]
    next1 = [int(center[0])+rayon,center[1]]
    for i in range(1,nbr_point+1):     
        new_angle = angle * i
        futur_point = next_point(center,new_angle,rayon)     
        pygame.draw.polygon(display,color,((center),next1,futur_point))
        next1 = futur_point
def next_point(center,angle,rayon):
    augment_y = math.sin(math.radians(angle))*rayon
    augment_x = math.cos(math.radians(angle))*rayon
    next_point = [int(center[0] + augment_x),int(center[1]-augment_y)]
    return next_point
    
        
        

        

