from feux1 import Firework
from feux1 import Explosion
from feux1 import drawcircle
import pretty_midi as pm

import testgrammar
import pygame
import random

pygame.init()

midi_path = "src\\audio_to_video\\media\\PinkPanther.midi"
midi = pm.PrettyMIDI(midi_path)

screen_height = 600
screen_width = 1000
display = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()
FPS = 90

fireworks = []
explosions = []
run = True

rules = testgrammar.Rules()  

rules.add_rule(testgrammar.Firework.Firework, [testgrammar.Symbol.MONTEE,testgrammar.Symbol.EXPLOSION])

rules.add_rule(testgrammar.Symbol.MONTEE, testgrammar.Terminal.LINEAIRE)
rules.add_rule(testgrammar.Symbol.MONTEE, testgrammar.Terminal.COURBER)

rules.add_rule(testgrammar.Symbol.EXPLOSION, testgrammar.Terminal.ETOILE)
rules.add_rule(testgrammar.Symbol.EXPLOSION, testgrammar.Terminal.PARTICULE)
rules.add_rule(testgrammar.Symbol.EXPLOSION, testgrammar.Terminal.METEORITE)


gen = testgrammar.Generator(rules)

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



while run:
    realtime = pygame.mixer.music.get_pos()/1000 
    for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    
    display.fill((0, 0, 0))
    
    while all_notes[note_number]<=realtime:
        result = gen.generate(testgrammar.Firework.Firework)
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
            

    pygame.display.update()
    clock.tick(FPS)
pygame.quit