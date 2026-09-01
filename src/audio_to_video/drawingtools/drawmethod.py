import math
import pygame

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


def draw_rectangle(display,color,x,y,longueur):
    centre = [x,y+longueur*2]
    point1 = [x-longueur/1.5,y+longueur]
    point2 = [x+longueur/1.5,y+longueur]
    point3 = [x+longueur/1.5,y+longueur*4]
    point4 = [x-longueur/1.5,y+longueur*4]
    pygame.draw.polygon(display,color,(centre,point1,point2))
    pygame.draw.polygon(display,color,(centre,point2,point3))
    pygame.draw.polygon(display,color,(centre,point3,point4))
    pygame.draw.polygon(display,color,(centre,point4,point1))


def draw_star(display,color,x,y,rayon):
    l1 = [x,y-(rayon/2)]
    l2 = [x+(rayon/2),y]
    l3 = [x-(rayon/2),y]
    l4 = [x,y+(rayon/2)]
    point1 = [x,y-rayon]
    point2 = [x+rayon,y]
    point3 = [x-rayon,y]
    point4 = [x,y+rayon]
    pygame.draw.polygon(display,color,(l2,l3,point1))
    pygame.draw.polygon(display,color,(l1,l4,point2))
    pygame.draw.polygon(display,color,(l1,l4,point3))
    pygame.draw.polygon(display,color,(l2,l3,point4))

def draw_rays(display,color,x,y,rayon,nbr_point):
    angle = 360/nbr_point
    new_angle = 0
    for i in range((nbr_point)):
        new_angle = angle * i
        augment_y = math.sin(math.radians(new_angle))*(rayon+10) 
        augment_x = math.cos(math.radians(new_angle))*(rayon+10)
        a = [x + augment_x,y - augment_y]
        augment_y1 = math.sin(math.radians(new_angle+10))*(rayon) 
        augment_x1 = math.cos(math.radians(new_angle+10))*(rayon) 
        b = [x+augment_x1,y-augment_y1]
        augment_y2 = math.sin(math.radians(new_angle-10))*(rayon)
        augment_x2 = math.cos(math.radians(new_angle-10))*(rayon) 
        c = [x+augment_x2,y-augment_y2]
        pygame.draw.polygon(display,color,(a,b,c))

def draw_background(display, x, y, rayon_max, couleur_proche, couleur_loin, nbr_anneaux, nbr_point):
    for i in range(nbr_anneaux, 0, -1):
        t = i / nbr_anneaux
        rayon = int(rayon_max * t)
        couleur = [int(c1 + (c2 - c1) * t) for c1, c2 in zip(couleur_proche, couleur_loin)]
        drawcircle(display, couleur, x, y, rayon, nbr_point)


        
        

        

