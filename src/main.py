import copy
import random

import pygame

from consts import *
import sys
from random import randint
from random import choice
from particle import Particle
from math import *
from copy import deepcopy

# Graphic Parameters
# window = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN | pygame.SCALED)
window = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


def rand_color() -> list[int]:
    return [randint(0, 255), randint(0, 255), randint(0, 255)]


def rand_particle() -> Particle:
    rand_pos = (randint(0, WINDOW_SIZE[0]), randint(0, WINDOW_SIZE[1]))
    return Particle(choice(P_COLORS), rand_pos)


def main():
    particle_radius = 1
    particles = [rand_particle() for _ in range(NUM_PARTICLES)]
    # particles = [Particle(WHITE, [130, 500]), Particle(PURPLE, [50, 500])]
    paused, show_radius = False, False
    # Randomly generate a matrix dictating attraction/repulsion between colors
    matrix = {}
    for color in P_COLORS:
        matrix[color] = {}
        for other_color in P_COLORS:
            matrix[color][other_color] = choice([-1, -.8, -.6, -.4, -.2, 0, 0.2, 0.4, 0.6, 0.8, 1])

    mouse_clicks = []
    while True:
        if not paused:
            # Data Manipulation (Model)
            # Apply the attractive/repulsive forces that dictate each particles velocity
            for particle in particles:
                particle.apply_force(particles, matrix)
            # Apply the calculated velocity to generate a new position for all particles
            for particle in particles:
                particle.update()
        # Event handler (Controller)
        for event in pygame.event.get():
            # keydown
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_e:
                    show_radius = not show_radius
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit(0)
                if event.key == pygame.K_1:
                    particle_radius = 1
                if event.key == pygame.K_2:
                    particle_radius = 2
                elif event.key == pygame.K_3:
                    particle_radius = 3

            # mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_clicks.append((mouse_pos, pygame.time.get_ticks()))
                for particle in particles:
                    r = sqrt(pow(mouse_pos[0] - particle.position[0], 2) + pow(mouse_pos[1] - particle.position[1], 2))
                    # if r > 100:
                    #     continue
                    delta_x, delta_y = mouse_pos[0] - particle.position[0], mouse_pos[1] - particle.position[1]
                    angle_radians = atan2(delta_y, delta_x)

                    particle.velocity[0] += 40 * cos(angle_radians)
                    particle.velocity[1] += 40 * sin(angle_radians)
            # Quit
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        # Rendering
        window.fill(BLACK)
        # Mouse
        for index, (pos, timestamp) in enumerate(mouse_clicks):
            pygame.draw.circle(window, WHITE, pos, 100, 1)
            if pygame.time.get_ticks() - timestamp > 100:
                mouse_clicks.pop(index)
        # Render particles
        for particle in particles:
            particle.render(window, particle_radius, show_radius)
        # Update screen
        pygame.display.flip()
        # Wait 17 ms
        clock.tick(60)


if __name__ == '__main__':
    main()
