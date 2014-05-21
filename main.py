import time

import pygame

from pygame.locals import *
from camz import surface, camera


surf = surface.FBSurface()
camera = camera.Camera()

camera.startRecording()

running = True

while running:
    cam = pygame.image.load(camera.captureStream())

    text = surf.font.render(time.ctime(), False, (255, 0, 0))
    
    cam.blit(text, (1,1))

    surf.display.blit(cam, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            running = False

camera.writeStream('test.h264')

camera.stopRecording()
