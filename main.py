#!/usr/bin/python
import time

import pygame

from pygame.locals import *
from camz import surface, camera

class Button(object):
    def __init__(self, text, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = surf.font.render(text, False, colorWhite)

    def draw(self, surface):
        pygame.draw.rect(surface, colorWhite,
            (self.x, self.y, self.w, self.h), 2)
        surface.blit(self.text, (self.x+15, self.y+12))

    def inside(self, x, y):
        inx = (x > self.x) and (y < (self.x+self.w))
        iny = (y > self.y) and (y < (self.y+self.h))

        if inx and iny:
            return True
        else:
            return False

    def sendEvent(self, event, surface):
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos

            if self.inside(x, y):
                pygame.draw.rect(surface, colorBlack, 
                    (self.x, self.y, self.w, self.h), 2)
                pygame.display.flip()
                return True

        return False


surf = surface.FBSurface()
camera = camera.Camera()

camera.startRecording()

running = True

colorWhite = (255,255,255)
colorBlack = (0,0,0)

store = Button('SAVE', 2, 200, 60, 40)
irnv = Button('IRNV', 258, 200, 60, 40)

buttons = [store, irnv]

while running:
    cam = camera.captureStream()

    uitime = surf.font.render(time.ctime(), False, colorWhite)
    cam.blit(uitime, (1,1))

    for button in buttons:
        button.draw(cam)

    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            running = False

        if store.sendEvent(event, cam):
            camera.writeStream('%s.h264' % time.strftime('%d-%m-%Y-%H%M%S'))

        if irnv.sendEvent(event, cam):
            if camera.irnv:
                camera.irnvOff()
            else:
                camera.irnvOn()

    surf.display.blit(cam, (0,0))
    pygame.display.flip()


camera.stopRecording()
