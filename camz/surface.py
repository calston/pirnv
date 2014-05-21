import pygame, sys, os
from pygame.locals import *


class FBSurface(object):
    def __init__(self):
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        pygame.init()
        pygame.mouse.set_visible(0)

        self.display = pygame.display.set_mode((320, 240), 0, 32)

        self.splash = pygame.image.load('images/pi_black_glow2.png').convert()

        self.display.blit(self.splash, (0,0))
        pygame.display.update()

        self.font = pygame.font.Font('freesansbold.ttf', 12)

