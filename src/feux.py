
import pygame
import random
import math

pygame.init()

display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
FPS = 90

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
    11 : (255,255,255),# blanc
    12 : (178,102,255),# mauve
}

def choose_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b
def get_color_from_note(note):
    valeur = note%13
    couleur = Color[int(valeur)]
    return couleur
class Streak():
    def __init__(self, x, y,type,note):
        self.color = get_color_from_note(note)
        self.type = 1
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.angle = random.uniform(-60, 240)
        velocity_mag = random.uniform(.3, 1.5)
        self.vx = velocity_mag*math.cos(math.radians(self.angle))  #velocity x
        self.vy = -velocity_mag*math.sin(math.radians(self.angle)) #velocity y
        self.timer = 0
        self.ended = False

    def get_angle(self):
        return math.atan2(-self.vy, self.vx)

    def move(self):
        if self.y < 550 :
            self.vy += 0.01
        self.x += self.vx
        self.y += self.vy
        self.timer += 1
        if self.timer >= 180:
            self.ended = True
        
    def drawtriangle(self):
        rayon = random.uniform(10,15)
        if self.type==1:
            angle = self.get_angle()
            length = 1
            dx = length*math.cos(angle)
            dy = length*math.sin(angle)
            a = [int(self.startx), int(self.starty)]
            b = [int(self.x-dx+10), int(self.y+dy)]
            c = [int(self.x-dx-10), int(self.y+dy)]
            pygame.draw.polygon(display, self.color, (a, b,c))
            drawCircle(20,self.x,self.y,10,self.color)
    

class Firework():
    def __init__(self,time,note):
        self.x = random.randint(0, 1000)
        self.y = 500
        self.distance = 400
        self.ended = False
        self.time = time
        self.timer = 0
        self.acceleration = (2*self.distance)/math.pow(self.time,2)
        self.initiale = 2*self.distance/self.time
        self.note = note
       


    def move(self):
        self.timer += 1/90
        self.vitesse = self.initiale -self.acceleration*self.timer
        self.y -= self.vitesse * 1/90
        if self.vitesse <= 0:
            self.ended = True
        
        
    def draw(self):
        a = [self.x, int(self.y-10)]
        b = [self.x-10, int(self.y+10)]
        c = [self.x+10, int(self.y+10)]
        pygame.draw.polygon(display, (128, 128, 128), (a, b,c),4)

def drawCircle(precision,x,y,rayon,color):
    centerx = x
    centery = y
    points = []
    for i in range(precision+1):
        angle = i *(360/precision)
        px = centerx + rayon * math.cos(math.radians(angle))
        py = centery - rayon * math.sin(math.radians(angle))
        points.append([px,py])
    for i in range(1,len(points)):
        p1 = points[i-1]
        p2 = points[i]
        pygame.draw.polygon(display, (color), ((centerx,centery),p1,p2))
    
        
def game():
    fireworks = [Firework(0.5,random.uniform(1,127))]
    streaks = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
        if random.uniform(0, 1) <= 1/60:
            fireworks.append(Firework(0.5,random.uniform(1,127)))
    
        display.fill((0, 0, 0))
        for firework in fireworks:
            firework.move()
            firework.draw()
            if firework.ended:
                streaks += [Streak(firework.x, firework.y,1,firework.note) for i in range(random.randint(20, 40))]
                fireworks.remove(firework)
        for streak in streaks:
            streak.move()
            streak.drawtriangle()
            if streak.ended:
                streaks.remove(streak)

        pygame.display.update()
        clock.tick(FPS)
        

game()
pygame.quit()