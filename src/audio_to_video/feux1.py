import random
import pygame
import math
import drawmethod

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

def choose_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b

class Firework():
    def __init__(self,time,display,pitch,ended_explosion,instrument,rise):
        if rise == "LINEAIRE":
            self.x = random.uniform(0,1000)
            self.distance = random.uniform(400,500)
        else: 
            self.distance = random.uniform(250,380)
            if random.uniform(0,1) < 0.5:
                self.x = random.randint(51, 300)
                
            else:
                self.x = random.randint(700, 899)
        self.y = 500
        
        self.time = time
        self.acceleration = 2*self.distance/math.pow(self.time,2)
        if 0 <= self.x <=500:
            self.angle = random.randint(60,80)
        else :
            self.angle = random.randint(100,120)
        if rise == "LINEAIRE":
            self.initial_speed = self.acceleration*self.time
        else:
            self.initial_speed = self.acceleration * self.time / math.sin(math.radians(self.angle))
        
        self.end = False
        self.display = display
        self.timer = 0
        self.color = get_note_from_pitch(pitch)
        self.color_particule = choose_random_color()
        self.ended_explosion = ended_explosion
        self.instrument = instrument
        self.longueur = 5
        self.trails = []
        self.rise = rise
        self.gravity = 2*self.distance/math.pow(self.time,2)
        
        
    def move(self):
        if self.rise =="LINEAIRE":
            self.speed = self.initial_speed-self.acceleration*self.timer
            self.y -= self.speed * 1/90
            if self.speed <= 0:
                    self.end = True
        if self.rise == "COURBER":
            self.speedx = self.initial_speed*math.cos(math.radians(self.angle))
            self.speedy = (self.gravity)*self.timer+self.initial_speed*-math.sin(math.radians(self.angle))
            self.x += self.speedx*1/90
            self.y += self.speedy*1/90
            if self.speedy >=0 :
                self.end = True
        self.trails.insert(0,Trail(self.x,self.y,(255,255,255),self.color_particule,self.display))
        if(len(self.trails) > 10):
            del self.trails[len(self.trails) - 1]
        
        for trail in self.trails:
            trail.update(999)
        self.timer += 1/90
        
    def draw(self):
        drawmethod.drawcircle(self.display,(255,255,255),self.x,self.y,2,10)
        #a = [self.x,self.y-self.longueur]
        #b = [self.x-self.longueur,self.y+self.longueur]
        #c = [self.x+self.longueur,self.y+self.longueur]
        #pygame.draw.polygon(self.display,(255,255,255),(a,b,c))
        #draw_rectangle(self.display,(255,255,255),self.x,self.y,self.longueur)

class Explosion():
    def __init__(self,display,x,y,color,color_particule,ended_explosion,instrument,rayon):
        self.x = x
        self.y = y
        self.angle = random.uniform(0,360)
        self.vx = math.cos(math.radians(self.angle)) * rayon
        self.vy = -math.sin (math.radians(self.angle)) * rayon
        self.color = color
        self.color_particule = color_particule
        self.end_time = ended_explosion
        self.timer = 0
        self.end = False
        self.display = display
        self.trails = []
        self.instrument = instrument

        
    def move(self):
        if self.y < 550 :
            self.vy += 0.0085
        if self.instrument =="METEORITE" or self.instrument=="PARTICULE":
            if self.timer%5==0:
                self.trails.insert(0,Trail(self.x,self.y,self.color,self.color_particule,self.display))
            if(len(self.trails) > 25):
                del self.trails[len(self.trails) - 1]
            for index, trail in enumerate(self.trails):
                trail.update(index)
        self.timer += 1
        self.x += self.vx
        self.y += self.vy
        if self.timer == self.end_time*90:
            self.end = True
    def draw(self):
        if self.instrument == "METEORITE":
            drawmethod.drawcircle(self.display,(self.color_particule),self.x,self.y,5,10)
        elif self.instrument =="ETOILE":
            drawmethod.draw_star(self.display,self.color,self.x,self.y,5)
        else:
            drawmethod.draw_star(self.display,(self.color_particule),self.x,self.y,5)
            
            
            
        


class Trail():
    def __init__(self,x,y,color,color_particule,display):
        self.x = x
        self.y = y 
        self.timer = 0
        self.color = color
        self.display = display
        self.exist = True
        self.a = [self.x,self.y-3]
        self.b = [self.x-3,self.y+3]
        self.c = [self.x+3,self.y+3]
        self.color_particule = color_particule
        pygame.draw.polygon(self.display,self.color_particule,(self.a,self.b,self.c))
    def update(self,index):
        self.timer += 1
        if self.timer == 40:
            self.exist=False
            self.timer = 0
        if not self.exist:
            return 
        self.a = [self.x,self.a[1]+0.05]
        self.b = [self.b[0]+0.05,self.b[1]-0.05]
        self.c = [self.c[0]-0.05,self.c[1]-0.05]
        if index>=5:
            pygame.draw.polygon(self.display,self.color,(self.a,self.b,self.c))
        else:
            pygame.draw.polygon(self.display,self.color_particule,(self.a,self.b,self.c))


