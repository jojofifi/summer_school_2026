from object.feux import Firework
from object.feux import Explosion
from tile import Tiles
import drawingtools.drawmethod as drawmethod
import pretty_midi as pm
import object.sunandmoon
import object.fireworkgrammar as fireworkgrammar
import pygame
import random

class Frontend:
    @staticmethod
    def start(midi_path, mp3_path):
        pygame.init()

        midi = pm.PrettyMIDI(midi_path)

        screen_height = 600
        screen_width = 1000
        display = pygame.display.set_mode((screen_width, screen_height))
        clock = pygame.time.Clock()
        FPS = 90

        fireworks = []
        explosions = []
        run = True

        rules = fireworkgrammar.Rules()

        rules.add_rule(fireworkgrammar.Firework.Firework, [fireworkgrammar.Symbol.MONTEE, fireworkgrammar.Symbol.EXPLOSION])

        rules.add_rule(fireworkgrammar.Symbol.MONTEE, fireworkgrammar.Terminal.LINEAIRE)
        rules.add_rule(fireworkgrammar.Symbol.MONTEE, fireworkgrammar.Terminal.COURBER)

        rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.ETOILE)
        rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.PARTICULE)
        rules.add_rule(fireworkgrammar.Symbol.EXPLOSION, fireworkgrammar.Terminal.METEORITE)
        Couleur = {
            0: (5, 10, 40),  # Nuit haut (bleu très sombre)
            1: (20, 25, 70),  # Nuit bas
            2: (60, 40, 70),  # Aube haut
            3: (200, 90, 60),  # Aube bas
            4: (255, 170, 60),  # Lever de soleil haut
            5: (255, 210, 120),  # Lever de soleil bas
        }

        liste_couleur = list(Couleur.values())
        nbr_transitions = len(liste_couleur) - 1
        duree_totale = midi.get_end_time()

        index_couleur = 0
        step = 1

        change_every_x_seconds = duree_totale / nbr_transitions
        number_of_steps = change_every_x_seconds * FPS


        gen = fireworkgrammar.Generator(rules)

        pygame.mixer.init()
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()

        flight_time = 1
        note_number = 0
        all_notes = []
        all_pitch = []

        for instrument in midi.instruments:
            for note in instrument.notes:
                all_notes.append(note.start - flight_time)
                all_pitch.append(note.pitch)


        combined = sorted(zip(all_notes, all_pitch))
        all_notes = [t for t, p in combined]
        all_pitch = [p for t, p in combined]
        moon = object.sunandmoon.Lune(display, -50, 200, 2 * (duree_totale / 4))
        sun = object.sunandmoon.Soleil(display, -50, 200, 2 * (duree_totale / 4))


        START_COORDINATES = (0, screen_height / 2)
        tiles = Tiles(START_COORDINATES, display, screen_height, screen_width, 125)
        mapTile = tiles.createTiles(45, 3)

        while run:
            realtime = pygame.mixer.music.get_pos() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            if realtime>=midi.get_end_time():
                run = False
            step += 1
            if step < number_of_steps:
                if index_couleur < nbr_transitions:
                    base_couleur = liste_couleur[index_couleur]
                    next_couleur = liste_couleur[index_couleur + 1]
                    current_color = [x + (((y - x) / number_of_steps) * step) for x, y in zip(base_couleur, next_couleur)]
            else:
                step = 1
                index_couleur += 1
                if index_couleur >= nbr_transitions:
                    current_color = liste_couleur[-1]

            display.fill((0, 0, 0))

            if not moon.end:
                moon.move()
                drawmethod.draw_background(display, moon.x, moon.y, 1150, base_couleur, next_couleur, 5, 10)
                moon.draw(base_couleur)

            else:
                sun.move()
                sun.draw()
                drawmethod.draw_background(display, sun.x, sun.y, 1150, base_couleur, next_couleur, 6, 10)
            sun.draw()

            while note_number <= (len(all_notes)-1) and all_notes[note_number] <= realtime:
                note_start = all_notes[note_number] + flight_time
                result = gen.generate(fireworkgrammar.Firework.Firework)
                style = result.children[1].children[0].value.name
                courbure = result.children[0].children[0].value.name
                if note_start < flight_time:
                    fireworks.append(Firework(note_start, display, all_pitch[note_number], 1, style, courbure))
                else:
                    fireworks.append(Firework(flight_time, display, all_pitch[note_number], 1, style, courbure))
                note_number += 1

            for firework in fireworks:
                firework.move()
                firework.draw()
                if firework.end:
                    if firework.instrument == "ETOILE":
                        for i in range(random.randint(15, 20)):
                            explosions.append(
                                Explosion(
                                    display,
                                    firework.x,
                                    firework.y,
                                    firework.color,
                                    firework.color_particule,
                                    firework.ended_explosion,
                                    firework.instrument,
                                    random.uniform(1, 0.25),
                                    current_color,
                                )
                            )
                    else:
                        for i in range(random.randint(20, 40)):
                            explosions.append(
                                Explosion(
                                    display,
                                    firework.x,
                                    firework.y,
                                    firework.color,
                                    firework.color_particule,
                                    firework.ended_explosion,
                                    firework.instrument,
                                    random.uniform(1, 0.75),
                                    current_color
                                )
                            )
                    fireworks.remove(firework)
                    del firework

            for each in mapTile:
                each.drawType()

            for explosion in explosions:
                explosion.move()
                explosion.draw()
                if explosion.end:
                    explosions.remove(explosion)
                    del explosion
            
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit
