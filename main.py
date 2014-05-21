import sys, os, io

import pygame
import picamera

from pygame.locals import *
from camz import surface


surf = surface.FBSurface()

camera = picamera.PiCamera()
camera.resolution = (800, 600)
camera.framerate = 30
camera.rotation = 180

while 1:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()

    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True, resize=(320, 240))
    stream.seek(0)
    cam = pygame.image.load(stream, 'jpeg').convert()
    
    surf.display_surface.blit(cam, (0,0))
    pygame.display.update()

