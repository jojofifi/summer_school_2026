
import pygame
import random
import math
import pretty_midi as pm
from collections import defaultdict
import time
pygame.init()

display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
FPS = 90
midi_path = "src\\Ecossaise_Beethoven.midi"
midi = pm.PrettyMIDI(midi_path)

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

def choose_random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b
def get_color_from_note(note):
    valeur = note%12
    couleur = Color[int(valeur)]
    return couleur
class Streak():
    def __init__(self, x, y,type,note,end_time):
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
        self.end_time = end_time

        self.all_point = []
        self.point_precision = 50

    def get_angle(self):
        return math.atan2(-self.vy, self.vx)

    def move(self):
        if self.y < 550 :
           self.vy += 0.01
        self.x += self.vx
        self.y += self.vy
        self.timer += 1
        if self.timer >= self.end_time:
            self.ended = True
        self.all_point.append((self.x,self.y))
        if len(self.all_point) > self.point_precision:
            self.all_point.pop(0)

    def drawtriangle(self):
        if self.type==1:
            n = len(self.all_point)
            angle = self.get_angle()
            length = 1
            dx = length*math.cos(angle)
            dy = length*math.sin(angle)
            a = [int(self.startx), int(self.starty)]
            b = [int(self.x-dx+10), int(self.y+dy)]
            c = [int(self.x-dx-10), int(self.y+dy)]
            for i, (px, py) in enumerate(self.all_point):
                ratio = (i + 1) / n 
                rayon = 3 * ratio
                drawCircle(3, px, py, rayon, self.color)
                i+=5      
            #pygame.draw.polygon(display, self.color, (a, b,c))    
            drawCircle(10,self.x,self.y,3,self.color)


class Firework():
    def __init__(self,time,note,streak_end):
        self.x = random.randint(0, 1000)
        self.y = 500
        self.distance = 400
        self.ended = False
        self.time = time
        self.timer = 0
        self.acceleration = (2*self.distance)/math.pow(self.time,2)
        self.initiale = 2*self.distance/self.time
        self.note = note
        self.streak_end = streak_end


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
    pygame.mixer.init()
    pygame.mixer.music.load(midi_path)
    pygame.mixer.music.play()
    t0 = time.time()
    all_notes = defaultdict(list)
    fireworks = []
    streaks = []
    flight_time = 0.5

    all_notes = []
    all_pitch = []
    all_duration = []
    for instrument in midi.instruments:
        for note in instrument.notes:
            all_notes.append(note.start-flight_time)
            all_pitch.append(note.pitch)
            all_duration.append(note.end-note.start)

    combined = sorted(zip(all_notes,all_pitch,all_duration))
    all_notes = [t for t, p, d in combined] 
    all_pitch = [p for t, p, d in combined]
    all_duration = [d for t, p, d in combined]
    note_number = 0

    first_note_time = min(note.start for instrument in midi.instruments for note in instrument.notes)
    print(f"Premiere note a  {first_note_time}")

    Max_streak = 500 
    

    while True:
        firework_per_frame = 0
        if not pygame.mixer.music.get_busy() and note_number >= len(all_notes):
            break
        realtime = pygame.mixer.music.get_pos()/1000 -0.3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        while pygame.mixer.music.get_pos()<0:
            pass

        while note_number < len(all_notes) and all_notes[note_number]<= realtime and firework_per_frame <= 4:
            fireworks.append(Firework(flight_time-0.1, all_pitch[note_number],all_duration[note_number]*130))
            note_number +=1
            firework_per_frame +=1
    
        display.fill((0, 0, 0))
        
        for firework in fireworks:
            firework.move()
            firework.draw()
            if firework.ended:
                if len(streaks) < Max_streak:
                    streaks += [Streak(firework.x, firework.y,1,firework.note,firework.streak_end) for i in range(random.randint(30, 50))]
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