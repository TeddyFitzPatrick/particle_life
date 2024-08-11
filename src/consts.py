import pygame
pygame.init()

# Monitor Dimensions
info = pygame.display.Info()

# Window Size (Fullscreen, 3/4-screen, 1/2-screen)
WINDOW_SIZE = [int(info.current_w), int(info.current_h)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (157, 0, 255)
PINK = (255, 192, 203)
LIGHT_BLUE = (20, 100, 250)

# Particle colors
P_COLORS = [WHITE, RED, ORANGE, GREEN, BLUE, PURPLE, PINK]
