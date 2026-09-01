from object.feux import Firework
from object.feux import Explosion
from tile import Tiles
import  drawingtools.drawmethod 
import pretty_midi as pm
import object.sunandmoon
import object.fireworkgrammar as fireworkgrammar
import pygame
import random


pygame.init()

midi_path = "media/PinkPanther.midi"
midi = pm.PrettyMIDI(midi_path)

screen_height = 600
screen_width = 1000
display = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
FPS = 90

fireworks = []
explosions = []
run = True

rules = fireworkgrammar.Rules()  

rules.add_rule(fireworkgrammar.Firework.Firework, [fireworkgrammar.Symbol.MONTEE,fireworkgrammar.Symbol.EXPLOSION])

rules.add_rule(fireworkgrammar.Symbol.MONTEE, fireworkgrammar.Terminal.LINEAIRE)
rules.add_rule(fireworkgrammar.Symbol.MONTEE, fireworkgrammar.Terminal.COURBER)

rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.ETOILE)
rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.PARTICULE)
rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.METEORITE)
Couleur = {
        0: (5, 10, 40),       # Nuit haut (bleu très sombre)
        1: (20, 25, 70),      # Nuit bas 
        2: (60, 40, 70),      # Aube haut 
        3: (200, 90, 60),     # Aube bas 
        4: (255, 170, 60),    # Lever de soleil haut
        5: (255, 210, 120),   # Lever de soleil bas 
}

liste_couleur = list(Couleur.values())
nbr_transitions = len(liste_couleur)-1
duree_totale = midi.get_end_time()

index_couleur = 0
step = 1

change_every_x_seconds = duree_totale / nbr_transitions 
number_of_steps = change_every_x_seconds * FPS



gen = fireworkgrammar.Generator(rules)

pygame.mixer.init()
pygame.mixer.music.load(midi_path)
pygame.mixer.music.play()

flight_time = 1
note_number = 0
all_notes = []
all_pitch = []

for instrument in midi.instruments:
    for note in instrument.notes:
        all_notes.append(note.start-flight_time)
        all_pitch.append(note.pitch)
        

combined = sorted(zip(all_notes,all_pitch))
all_notes = [t for t, p in combined] 
all_pitch = [p for t, p in combined]
moon = object.sunandmoon.Lune(display,-50,200,3*(duree_totale/5))
sun = object.sunandmoon.Soleil(display,-50,200,2*(duree_totale/5))


START_COORDINATES = (0,screen_height/2)
tiles = Tiles(START_COORDINATES, display, screen_height, screen_width, 130)
mapTile = tiles.createTiles(42,4)

while run:
    realtime = pygame.mixer.music.get_pos()/1000 
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    step += 1
    if step < number_of_steps:
        if index_couleur < nbr_transitions:
            base_couleur = liste_couleur[index_couleur]
            next_couleur = liste_couleur[index_couleur + 1]
            current_color = [x + (((y-x)/number_of_steps)*step) for x, y in zip(base_couleur,next_couleur)]
    else:
        step=1
        index_couleur += 1
        if index_couleur >= nbr_transitions:
            current_color = liste_couleur[-1]

    display.fill((0,0,0))
    
    
    if not moon.end:
        moon.move()
        drawingtools.drawmethod.draw_background(display,moon.x,moon.y,1150,base_couleur,next_couleur,15,15)
        moon.draw(base_couleur)
        
    else:
        sun.move()
        sun.draw()
        drawingtools.drawmethod.draw_background(display,sun.x,sun.y,1150,base_couleur,next_couleur,15,15)
    sun.draw()      
    while all_notes[note_number]<=realtime:
        result = gen.generate(fireworkgrammar.Firework.Firework)
        style = result.children[1].children[0].value.name
        courbure = result.children[0].children[0].value.name  
        fireworks.append(Firework(flight_time,display,all_pitch[note_number],1,style,courbure))
        note_number += 1

        

    for firework in fireworks:
        firework.move()
        firework.draw()
        if firework.end:
            for i in range(random.randint(20,40)):
                if not firework.instrument=="METEORITE":
                    explosions.append(Explosion(display,firework.x,firework.y,firework.color,firework.color_particule,firework.ended_explosion,firework.instrument,random.uniform(1,0.75)))
                    explosions.append(Explosion(display,firework.x,firework.y,firework.color,firework.color_particule,firework.ended_explosion,firework.instrument,random.uniform(0.75,0.5)))
                    explosions.append(Explosion(display,firework.x,firework.y,firework.color,firework.color_particule,firework.ended_explosion,firework.instrument,random.uniform(0.5,0.25)))
                else:
                     explosions.append(Explosion(display,firework.x,firework.y,firework.color,firework.color_particule,firework.ended_explosion,firework.instrument,random.uniform(1,0.75)))                 
            fireworks.remove(firework)
            del firework
    for explosion in explosions:
        explosion.move()
        explosion.draw()
        if explosion.end:
            explosions.remove(explosion)
            del explosion

    for each in mapTile:
        each.drawType()

    pygame.display.update()
    clock.tick(FPS)
pygame.quit