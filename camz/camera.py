import io
import picamera
import pygame

from PIL import Image, ImageOps

class Camera(object):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1296,730)
        self.camera.rotation = -90
        self.camera.led = False
        self.camera.shutter_speed = 0
        self.camera.video_stabilization = True

        self.recording = False

        self.loopStream = picamera.PiCameraCircularIO(self.camera, size=128*1024*1024)

        self.irnv = False

    def irnvOn(self):
        self.irnv = True
        self.camera.color_effects = (128, 128)
        self.camera.contrast = 10
        self.camera.brightness = 55
        self.camera.exposure_mode = 'night'
        self.ledOn()

    def irnvOff(self):
        self.irnv = False
        self.camera.color_effects = None
        self.camera.contrast = 0
        self.camera.brightness = 50
        self.camera.exposure_mode = 'auto'
        self.ledOff()
 
    def ledOn(self):
        self.camera.led = True

    def ledOff(self):
        self.camera.led = False
    
    def captureStream(self, width=320, height=240):
        stream = io.BytesIO()

        self.camera.capture(stream, format='jpeg', use_video_port=True,
            resize=(width, height))
        stream.seek(0)

        return pygame.image.load(stream).convert()

    def startRecording(self):
        self.camera.start_recording(self.loopStream, format='h264')
        self.recording = True

    def stopRecording(self):
        self.camera.stop_recording()
        self.recording = False

    def writeStream(self, filename):
        if not self.recording:
            return
        
        with self.loopStream.lock:
            for frame in self.loopStream.frames:
                if frame.header:
                    self.loopStream.seek(frame.position)
                    break

            with open(filename, 'wb') as output:
                output.write(self.loopStream.read())

        self.loopStream.seek(0)
        self.loopStream.truncate()

