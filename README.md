# PiRNV

PiRNV is a Python loop recording application for Raspberry Pi, using picamera and pygame.

This creates a 10 minute ring buffer (which there's hopefully enough free memory to hold), and writes a recording only when required. 

It also captures frames from the camera video stream and draws them to the linux framebuffer (which in my case is a touchscreen LCD). 
