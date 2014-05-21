import io
import picamera

class Camera(object):
    def __init__(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (800, 600)
        self.camera.framerate = 30
        self.camera.rotation = 180
        self.camera.led = False

        self.recording = False

        self.loopStream = picamera.PiCameraCircularIO(self.camera, seconds=600)
    
    def captureStream(self):
        if self.recording:
            self.camera.wait_recording()

        stream = io.BytesIO()
        self.camera.capture(stream, format='jpeg', use_video_port=True, resize=(320, 240))
        stream.seek(0)
        
        return stream

    def startRecording(self):
        self.camera.start_recording(self.loopStream, format='h264')
        self.recording = True

    def stopRecording(self):
        self.camera.stop_recording()
        self.recording = False

    def writeStream(self, filename):
        if not self.recording:
            return

        with io.open(filename, 'wb') as output:
            for frame in self.loopStream.frames:
                if frame.header:
                    self.loopStream.seek(frame.position)
                    break
            while True:
                buf = stream.read1()
                if not buf:
                    break
                output.write(buf)
        self.loopStream.seek(0)
        self.loopStream.truncate()

