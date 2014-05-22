import io
import picamera
import pygame

from PIL import Image, ImageOps

class Camera(object):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1296,730)
        self.camera.rotation = 180
        self.camera.led = False

        self.recording = False

        self.loopStream = picamera.PiCameraCircularIO(self.camera, size=128*1024*1024)
    
    def captureStream(self, irnv=True, width=320, height=240):
        stream = io.BytesIO()

        if irnv:
            self.camera.capture(stream, format='jpeg', use_video_port=True,
                resize=(width, height))
            stream.seek(0)

            image = Image.open(stream).convert('LA').convert('RGBA')

            return pygame.image.fromstring(image.tostring(), image.size, image.mode)

        else:
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

