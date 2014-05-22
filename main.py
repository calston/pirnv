import time

import pygame

from pygame.locals import *
from camz import surface, camera


surf = surface.FBSurface()
camera = camera.Camera()

camera.startRecording()

running = True

colorWhite = (255,255,255)
colorBlack = (0,0,0)

store = surf.font.render('SAVE', False, colorWhite)
irnv = surf.font.render('IRNV', False, colorWhite)

irnv_mode = False

while running:
    cam = camera.captureStream(irnv=irnv_mode)

    text = surf.font.render(time.ctime(), False, colorWhite)
    
    cam.blit(text, (1,1))

    # Save button
    pygame.draw.rect(cam, colorWhite, (2, 200, 60, 40), 2)
    cam.blit(store, (17, 212))

    # IRNV button
    pygame.draw.rect(cam, colorWhite, (258, 200, 60, 40), 2)
    cam.blit(irnv, (273, 212))

    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            running = False

        if event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos
            
            if (mx > 2) and (mx <62) and (my > 200) and (my < 240):
                pygame.draw.rect(cam, colorBlack, (2, 200, 60, 40), 2)
                surf.display.blit(cam, (0,0))
                pygame.display.flip()
                camera.writeStream('%s.h264' % time.strftime('%d-%m-%Y-%H%M%S'))

            if (mx > 258) and (mx <320) and (my > 200) and (my < 240):
                pygame.draw.rect(cam, colorBlack, (258, 200, 60, 40), 2)
                irnv_mode = not irnv_mode


    surf.display.blit(cam, (0,0))
    pygame.display.flip()


camera.stopRecording()
