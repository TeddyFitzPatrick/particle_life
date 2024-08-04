import pygame
pygame.init()

# Screen
info = pygame.display.Info()
WINDOW_SIZE = [int(info.current_w/2), int(info.current_h/2)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (157, 0, 255)
PINK = (255, 192, 203)


# Arbitrary Particle Life Constants
R_MAX = 100
R_MIN = 20
R_ZENITH = (R_MIN + R_MAX) / 2


NUM_PARTICLES = 400
P_COLORS = [WHITE, RED, ORANGE, GREEN, BLUE, PURPLE, PINK]
