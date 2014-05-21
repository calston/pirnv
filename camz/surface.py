import pygame, sys, os
from pygame.locals import *


class FBSurface(object):
    def __init__(self):
        os.environ["SDL_FBDEV"] = "/dev/fb1"
        pygame.init()
        pygame.mouse.set_visible(0)

        self.display_surface = pygame.display.set_mode((320, 240), 0, 32)

        self.display_surface.fill((255,255,255))

        self.splash = pygame.image.load('images/pi_black_glow2.png').convert()

        self.display_surface.blit(self.splash, (0,0))
       
        pygame.display.flip()
