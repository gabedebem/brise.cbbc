from picamera import PiCamera
from time import sleep

camera = PiCamera ()
camera.rotation = 180

camera.start_preview ()
sleep (5)
camera.start_recording ('/home/pi/brise.cbbc/images/video.h264')
camera.stop_recording ()
camera.stop_preview ()